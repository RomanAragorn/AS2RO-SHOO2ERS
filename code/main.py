import pygame, sys, os
from player import Player
from enemy import Enemy
from random import randint, choice
from laser import Laser
from menu import Menu, High_Scores, Pause, Game_Over
from score import show_highscore_window, handle_fresh_file
from timer import Timer 
from drops import Drop
from boss import Boss


#================Main Menu===============#
# Start Game

# Exit Game


# Menu Selection


# Main function for the Menu
def main():
    pygame.init()
    handle_fresh_file()

    screen_width, screen_height = 1920, 1080
    screen = pygame.display.set_mode((screen_width, screen_height))

    menu = Menu(screen, screen_width, screen_height)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    menu.selected_item = (menu.selected_item - 1) % len(menu.menu_items)
                elif event.key == pygame.K_DOWN:  
                    menu.selected_item = (menu.selected_item + 1) % len(menu.menu_items)
                elif event.key == pygame.K_RETURN: 
                    running = handle_menu_selection(menu, screen)  # Pass the screen to the handler

        screen.fill((0, 0, 0))
        menu.run()
        pygame.display.flip()

    pygame.quit()

# runs main    

#-----------------------------------------------------------------------------------------#
#==================== Game Logic =====================================#

# Game elements
class Game:
    def __init__(self):

        handle_fresh_file()

        # Player setup
        player_sprite = Player((display_width/2, display_height - 50), display_width/2 + screen_width/2, 8)
        self.player = pygame.sprite.GroupSingle(player_sprite)
        self.player_surface = pygame.Surface((50,50))
        self.player_mask = pygame.mask.from_surface(self.player_surface)

        # Enemy setup
        self.spawn_enemy_start = False
        self.enemies = pygame.sprite.Group()
        self.enemy_lasers = pygame.sprite.Group()
        self.spawn_enemy_ready = True
        self.spawn_enemy_time = 0
        self.spawn_enemy_timer = 150
        self.current_time = 0
        self.boss = pygame.sprite.GroupSingle()

        # Score setup
        self.score = 0
        self.font = pygame.font.Font('font\\Pixeled.ttf', 15)
        self.maj_font = pygame.font.Font('font\\Pixeled.ttf', 30)
        self.combo = 0
        self.combo_bonus = 0

        # Audio setup
        self.music = pygame.mixer.Sound('audio\\music.wav')
        self.music.set_volume(0)
        self.music.play(loops=-1)

        self.laser_audio = pygame.mixer.Sound('audio\\laser.wav')
        self.laser_audio.set_volume(0)

        self.explosion_audio = pygame.mixer.Sound('audio\\explosion.wav')
        self.explosion_audio.set_volume(0)

        # Game state
        self.menu_running = True
        self.game_running = False
        self.game_over = False
        self.high_scores_running = False
        self.selection = 0  # 0 for Restart, 1 for Quit
        self.is_paused = False
        
        # Game clock
        self.tick = 60
        self.runtime = 0

        # For game over screen
        self.selection_timer = 100
        self.selection_time = 0

        # Drops
        self.drop_rate = 0.3
        self.drops = pygame.sprite.Group()

        # Shield functionality
        self.shield_max_amount = 3
        self.shield_amount = 3
        self.shield_time = 0
        self.shield_cooldown = 100 
        self.shield_duration = 2000
        self.is_shielded = False

        # Timers
        self.timers = {
            'shield' : Timer(1500, func = self.toggle_shield),
            'spawn_boss': Timer(10000, func = self.spawn_boss),
            'spawn_enemies': Timer(2000, func = self.spawn_enemy_flag)
        }

        # Arcade 
        self.arcade = Arcade()
        self.CRT = CRT()
        self.flicker = Arcade_Flicker()

        # Menu
        self.menu = Menu(screen, display_width, display_height)
        self.high_scores = High_Scores(screen, display_width, display_height)
        self.pause_menu = Pause(screen, display_width, display_height)
        self.game_over_menu = Game_Over(screen, display_width, display_height)

        # Layers
        self.layers = pygame.sprite.LayeredUpdates()

    def start_game(self):
        print("Game started!")
        self.menu_running = False
        self.game_running = True
        self.timers['spawn_boss'].activate()
        self.timers['spawn_enemies'].activate()

    def quit_game(self):
        pygame.quit()  # Quit pygame
        sys.exit()  # Exit program
    
    def show_highscores(self):
        self.menu_running = False
        self.high_scores_running = True

    def handle_menu_selection(self):
            if self.menu.menu_items[self.menu.selected_item] == "Start Game":
                self.start_game()  
                return False 
            
            elif self.menu.menu_items[self.menu.selected_item] == "High Scores":
                self.show_highscores()
                return False

            elif self.menu.menu_items[self.menu.selected_item] == "Quit":
                self.quit_game()  
            return True  
    
    def handle_game_over_selection(self):
            if self.game_over_menu.menu_items[self.game_over_menu.selected_item] == "Restart":
                self.reset_game()  
                return False 
                
            elif self.game_over_menu.menu_items[self.game_over_menu.selected_item] == "Menu":
                self.game_running = False
                self.game_over = False
                self.menu_running = True
                return False

            elif self.game_over_menu.menu_items[self.game_over_menu.selected_item] == "Quit":
                self.quit_game()  
            return True  
    
    def spawn_enemy_flag(self):
        self.spawn_enemy_start = not self.spawn_enemy_start

    def spawn_enemy(self):
        if self.spawn_enemy_ready:
            has_drop = False
            enemy_color = choice(['pink', 'green', 'blue'])
            will_drop = randint(0, 1)
            if will_drop <= self.drop_rate:
                has_drop = True
            if enemy_color == 'green':
                x = randint(760, 1160 - 100)
            else:
                x = randint(760, 1160 - 50)
            self.spawn_enemy_time = self.runtime
            self.enemies.add(Enemy(enemy_color, x, display_height, self.spawn_enemy_time, has_drop))
            self.spawn_enemy_ready = False

    def spawn_enemy_reset(self):
        if not self.spawn_enemy_ready:
            self.current_time = self.runtime
            if self.current_time - self.spawn_enemy_time >= self.spawn_enemy_timer:
                self.spawn_enemy_ready = True

    def spawn_boss(self):
        spawn_time = pygame.time.get_ticks()
        self.boss.add(Boss(100, spawn_time, has_drop=True))

    def enemy_shoot(self):
        if self.enemies.sprites():
            for enemy in self.enemies.sprites():
                if enemy.color == 'pink':
                    laser = Laser(enemy.rect.center, -4, display_height)
                    self.laser_audio.play()  # Play laser sound
                    self.enemy_lasers.add(laser)
    
    def damaged(self):
        screen.fill((255, 0, 255))

    def increment_point_flag(self):
        if self.player.sprite.point_flag <= 4:
            if self.score >= 100 and self.score < 500: 
                self.player.sprite.point_flag = 1
                self.player.sprite.laser_cooldown = 600 - (self.player.sprite.point_flag * 100)
            elif self.score >= 500 and self.score < 1000:
                self.player.sprite.point_flag = 2
                self.player.sprite.laser_cooldown = 600 - (self.player.sprite.point_flag * 100)     
            elif self.score >= 1000 and self.score < 1500:
                self.player.sprite.point_flag = 3
                self.player.sprite.laser_cooldown = 600 - (self.player.sprite.point_flag * 100)
            elif self.score >= 1500 and self.score < 2000:
                self.player.sprite.point_flag = 4
                self.player.sprite.laser_cooldown = 600 - (self.player.sprite.point_flag * 100)
            elif self.score >= 2000:
                self.player.sprite.point_flag = 5
                self.player.sprite.laser_cooldown = 600 - (self.player.sprite.point_flag * 100)

    def toggle_shield(self):
        self.is_shielded = not self.is_shielded

    def shield_up(self):
        if self.shield_amount > 0: 
            self.toggle_shield()
            self.timers['shield'].activate()
            self.shield_amount -= 1

    def shielded(self):
        if self.is_shielded:
            self.player.sprite.image = pygame.image.load('images\\shield.png').convert_alpha()
            self.player.sprite.image = pygame.transform.scale(self.player.sprite.image, (50, 50))
        else:
            self.player.sprite.image = pygame.image.load('images\\player.png').convert_alpha()
            self.player.sprite.image = pygame.transform.scale(self.player.sprite.image, (50, 50))
            
    def update_timers(self):
        for timer in self.timers.values(): 
            timer.update()

    def reset_timers(self):
        self.timers['spawn_boss'].activate()
        self.timers['spawn_enemies'].activate()

    def collision_check(self):
        # Player lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                enemy_hit = pygame.sprite.spritecollide(laser, self.enemies, False)
                if enemy_hit:
                    if pygame.sprite.spritecollide(laser, self.enemies, False, pygame.sprite.collide_mask):
                        for enemy in enemy_hit:
                            enemy.health -= 1
                            if enemy.health <= 0:
                                if enemy.has_drop:
                                    drop_type = choice(['health', 'shield'])
                                    self.drops.add(Drop(drop_type, display_height, enemy.rect.center))
                                enemy.kill()
                                if self.combo <= 29:
                                    self.combo += 1
                                    self.combo_bonus = self.combo * 10
                                self.score += (enemy.value + self.combo_bonus)
                        self.explosion_audio.play()  # Play explosion sound
                        laser.kill()
                boss_hit = pygame.sprite.spritecollide(laser, self.boss, False)
                if boss_hit:
                    if pygame.sprite.spritecollide(laser, self.boss, False, pygame.sprite.collide_mask): 
                        self.boss.sprite.health -= 1
                        if self.boss.sprite.health <= 0:
                            if self.combo <= 29:
                                    self.combo += 1
                                    self.combo_bonus = self.combo * 10
                            self.score += (self.boss.sprite.value + self.combo_bonus)
                            self.boss.sprite.kill()
                            self.timers['spawn_boss'].activate()
                        self.explosion_audio.play()
                        laser.kill()

        # Enemy lasers
        if self.enemy_lasers:
            for laser in self.enemy_lasers:
                if pygame.sprite.spritecollide(laser, self.player, False):
                    if pygame.sprite.spritecollide(laser, self.player, False, pygame.sprite.collide_mask):
                        if not self.is_shielded:
                            self.player.sprite.health -= 1
                            self.damaged()
                            self.combo = 0
                            self.combo_bonus = self.combo * 10
                        if self.player.sprite.health <= 0:
                            self.game_over = True
                            self.game_running = False  # Set game over state
                            self.handle_high_scores()
                        self.explosion_audio.play()  # Play explosion sound
                        laser.kill()

        # Enemy collisions
        if self.enemies:
            for enemy in self.enemies:
                if pygame.sprite.spritecollide(enemy, self.player, False):
                    if pygame.sprite.spritecollide(enemy, self.player, False, pygame.sprite.collide_mask):
                        if not self.is_shielded:
                            self.player.sprite.health -= 1
                            self.damaged()
                            self.combo = 0
                            self.combo_bonus = self.combo * 10
                        if self.player.sprite.health <= 0:
                            self.game_over = True
                            self.game_running = False # Set game over state
                            self.handle_high_scores()  
                        self.explosion_audio.play()  # Play explosion sound
                        enemy.kill()

        # Boss moves collisions
        if self.boss:
            if self.boss.sprite.move_sprites:
                for fist in self.boss.sprite.move_sprites:
                    if pygame.sprite.spritecollide(fist, self.player, False):
                        if pygame.sprite.spritecollide(fist, self.player, False, pygame.sprite.collide_mask):
                            if not self.is_shielded:
                                self.player.sprite.health -= 1
                                self.damaged()
                                self.combo = 0
                                self.combo_bonus = self.combo * 10
                            if self.player.sprite.health <= 0:
                                self.game_over = True
                                self.game_running = False  # Set game over state
                                self.handle_high_scores()
                            self.explosion_audio.play()  # Play explosion sound
                            fist.kill()       


        # Drop collisions
        if self.drops: 
            for drop in self.drops: 
                if pygame.sprite.spritecollide(drop, self.player, False):
                    if pygame.sprite.spritecollide(drop, self.player, False, pygame.sprite.collide_mask):
                        if drop.type == 'health':
                            if self.player.sprite.health < self.player.sprite.max_health:
                                self.player.sprite.health += 1
                        elif drop.type == 'shield':
                            if self.shield_amount < self.shield_max_amount:
                                self.shield_amount += 1
                        drop.kill()
    def display_score(self):
        score_surf = self.font.render(f'{self.score}', False, 'white')
        score_rect = score_surf.get_rect(topleft=(arcade_screen_left + 10, arcade_screen_top))
        screen.blit(score_surf, score_rect)

    def display_lives(self):
        lives_surf = self.font.render(f'Lives: {self.player.sprite.health}', False, 'white')
        lives_rect = lives_surf.get_rect(bottomleft=(arcade_screen_left - 10, arcade_screen_bottom - 50))
        screen.blit(lives_surf, lives_rect)
    
    def display_combo(self):
        if self.combo > 0: 
            combo_surf = self.font.render(f'Combo: {self.combo}', False, 'white')
            combo_rect = combo_surf.get_rect(topleft=(arcade_screen_left + 9, arcade_screen_top + 50))
            screen.blit(combo_surf, combo_rect)
    
    def display_shield(self):
        shield_surf = self.font.render(f'Shield: {self.shield_amount}', False, 'white')
        shield_rect = shield_surf.get_rect(bottomleft=(arcade_screen_left - 10, arcade_screen_bottom))
        screen.blit(shield_surf, shield_rect)

    def display_game_over_score(self):
        self.high_scores.read_highscores()
        game_over_score_text = self.font.render(f"Your Score: {self.score}", True, (255, 255, 255))
        
        game_over_score_rect = game_over_score_text.get_rect(center=(display_width / 2, display_height / 2))
      
        screen.blit(game_over_score_text, game_over_score_rect)

    def handle_high_scores(self):
        with open('records\\high_scores.txt', 'r') as file:
            current_scores = file.read()

        new_contents = str(self.score).zfill(10) + current_scores

        with open('records\\high_scores.txt', 'w') as file: 
            file.write(new_contents)

        os.system("code\\high_score")
        os.system("code\\move_to_hs")
    
    def reset_game(self):
        # Reset all variables to their initial states 
        self.game_running = True
        player_sprite = Player((display_width/2, display_height - 50), display_width/2 + screen_width/2, 8)
        self.player = pygame.sprite.GroupSingle(player_sprite)
        self.enemies.empty()
        self.enemy_lasers.empty()
        self.drops.empty()
        self.boss.empty()
        self.reset_timers()
        self.score = 0
        self.game_over = False
        self.selection = 0  # Reset selection to "Restart"
        self.runtime = 0
        self.current_time = 0
        self.spawn_enemy_time = 0
        self.spawn_enemy_start = False

        # Restart the background music and SFX when the game restarts
        
        self.laser_audio.set_volume(0.1)  # Ensure laser audio is enabled again
        self.explosion_audio.set_volume(0.5)  # Ensure explosion audio is enabled again

    def pause_game(self):
        #self.game_running = not self.game_running
        self.is_paused = not self.is_paused

    def add_to_layers(self):
        pass
    def run(self):
        if self.game_over:
            self.game_over_menu.run()
            self.display_game_over_score()

        # Update 
        # Is inside of an if-else because the game runs normally otherwise
        if self.menu_running:
            self.menu.run()
        elif self.high_scores_running:
            self.high_scores.run()
        elif self.game_running:
            # Spawn enemies
            if self.spawn_enemy_start:
                self.spawn_enemy()
                self.spawn_enemy_reset()

            self.player.draw(screen)
            self.player.sprite.lasers.draw(screen)
            self.enemies.draw(screen)
            self.enemy_lasers.draw(screen)
            self.drops.draw(screen)
            self.display_score()
            self.display_lives()
            self.display_combo()
            self.display_shield()
            self.runtime += 1
            if self.boss:
                self.boss.draw(screen)
                self.boss.sprite.move_sprites.draw(screen)
            
            if self.is_paused == False:
            # Collision checking
                self.collision_check()
                self.player.update()
                self.enemies.update()
                self.enemy_lasers.update()
                self.increment_point_flag()
                self.drops.update()
                self.update_timers()
                self.shielded()
                self.boss.update()
            elif self.is_paused == True: 
                # Display pause menu 
                self.pause_menu.run()
        
        self.CRT.draw()
        self.arcade.draw()
        self.flicker.draw()
        
            
# For extra graphics
class CRT(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
    self.tv = pygame.image.load('images\\tv.png').convert_alpha()
    self.tv = pygame.transform.scale(self.tv, (1920, 1080))
    self.rect = self.tv.get_rect(center=(display_width / 2, display_height / 2))

  def create_lines(self):
    line_height = 3
    line_amount = int(display_height/line_height)
    for line in range(line_amount):
      y_pos = line * line_height
      pygame.draw.line(self.tv,'black',(0, y_pos),(display_width, y_pos), 1)

  def draw(self):
    self.tv.set_alpha(randint(75,90))
    self.create_lines()
    screen.blit(self.tv, self.rect)

class Arcade(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.arcade = pygame.image.load('images\\arcade.png').convert_alpha()
        self.arcade = pygame.transform.scale(self.arcade, (1920, 1080))
    
    def draw(self):
        screen.blit(self.arcade, (0,0))

class Arcade_Flicker(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.flicker = pygame.image.load('images\\flicker.png').convert_alpha()
        self.flicker = pygame.transform.scale(self.flicker, (1920, 1080))
        self.rect = self.flicker.get_rect(center=(display_width / 2, display_height / 2))
    
    def draw(self):
        self.flicker.set_alpha(randint(10, 15))
        screen.blit(self.flicker, self.rect)
# Main game loop
if __name__ == '__main__':
  pygame.init()
  display_width = 1920
  display_height = 1080
  screen_width = 400
  screen_height = 800
  arcade_screen_left = 660
  arcade_screen_right = 1260
  arcade_screen_top = display_height - 770
  arcade_screen_bottom = display_height - 50
  screen = pygame.display.set_mode((display_width, display_height))
  clock = pygame.time.Clock()
  
  game_running = False
  menu_running = True
  game_over_running = False
  game = Game()
  ENEMYLASER = pygame.USEREVENT + 1
  pygame.time.set_timer(ENEMYLASER, 2000)

  running = True
  # Main loop
  while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game.menu_running: 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.menu.selected_item = (game.menu.selected_item - 1) % len(game.menu.menu_items)
                elif event.key == pygame.K_DOWN:  
                    game.menu.selected_item = (game.menu.selected_item + 1) % len(game.menu.menu_items)
                elif event.key == pygame.K_RETURN: 
                    game.menu_running = game.handle_menu_selection()  # Pass the screen to the handler
        elif game.high_scores_running:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Press ESC to return to the main menu
                    game.high_scores_running = False
                    game.menu_running = True
        elif game.game_running:
            if not game.is_paused: 
                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_ESCAPE:
                        game.pause_game()
            elif game.is_paused:
                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_RETURN:
                        game.pause_game()
        elif game.game_over:
             if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.game_over_menu.selected_item = (game.game_over_menu.selected_item - 1) % len(game.game_over_menu.menu_items)
                elif event.key == pygame.K_DOWN:  
                    game.game_over_menu.selected_item = (game.game_over_menu.selected_item + 1) % len(game.game_over_menu.menu_items)
                elif event.key == pygame.K_RETURN: 
                    game.game_over = game.handle_game_over_selection() # Pass the screen to the handler

        if event.type == ENEMYLASER:
            game.enemy_shoot()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:      
                game.shield_up()
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

    screen.fill((30,30,30))
    
    game.run()
    
    pygame.display.flip()
    clock.tick(game.tick)