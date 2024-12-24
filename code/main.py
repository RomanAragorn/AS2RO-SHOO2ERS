import pygame, sys, os
from player import Player
from enemy import Enemy
from random import randint, choice
from laser import Laser
from menu import Menu
from score import show_highscore_window, handle_fresh_file

#================Main Menu===============#
# Start Game
def start_game():
    print("Game started!")
   
# Exit Game
def quit_game():
    pygame.quit()  # Quit pygame
    sys.exit()  # Exit program

# Menu Selection
def handle_menu_selection(menu, screen):
    if menu.menu_items[menu.selected_item] == "Start Game":
        start_game()  
        return False 
     
    elif menu.menu_items[menu.selected_item] == "High Scores":
        show_highscore_window(screen)  # Call the function from high.py

    elif menu.menu_items[menu.selected_item] == "Quit":
        quit_game()  
    return True  

# Main function for the Menu
def main():
    pygame.init()
    handle_fresh_file()

    screen_width, screen_height = 800, 600
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
if __name__ == "__main__":
    main()

#-----------------------------------------------------------------------------------------#
#==================== Game Logic =====================================#

# Game elements
class Game:
    def __init__(self):
        # Player setup
        player_sprite = Player((screen_width / 2, screen_height), screen_width, 8)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # Enemy setup
        self.enemies = pygame.sprite.Group()
        self.enemy_lasers = pygame.sprite.Group()
        self.spawn_enemy_ready = True
        self.spawn_enemy_time = 0
        self.spawn_enemy_timer = 1500

        # Score setup
        self.score = 0
        self.font = pygame.font.Font('font\\Pixeled.ttf', 20)
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
        self.running = True
        self.game_over = False
        self.selection = 0  # 0 for Restart, 1 for Quit
        
        # Game clock
        self.tick = 60

        # Extra windows
        self.pause_menu = pygame.Surface((screen_width, screen_height))
        self.pause_menu.fill((0, 0, 0))
        self.pause_menu.set_alpha(90)

    def spawn_enemy(self):
        if self.spawn_enemy_ready:
            enemy_color = choice(['pink', 'green', 'blue'])
            if enemy_color == 'green':
                x = randint(50, screen_width - 100)
            else:
                x = randint(50, screen_width - 50)
            self.spawn_enemy_time = pygame.time.get_ticks()
            self.enemies.add(Enemy(enemy_color, x, screen_height, self.spawn_enemy_time))
            self.spawn_enemy_ready = False

    def spawn_enemy_reset(self):
        if not self.spawn_enemy_ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.spawn_enemy_time >= self.spawn_enemy_timer:
                self.spawn_enemy_ready = True

    def enemy_shoot(self):
        if self.enemies.sprites():
            for enemy in self.enemies.sprites():
                if enemy.color == 'pink':
                    laser = Laser(enemy.rect.center, -4, screen_height)
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
    def collision_check(self):
        # Player lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                enemy_hit = pygame.sprite.spritecollide(laser, self.enemies, False)
                if enemy_hit:
                    for enemy in enemy_hit:
                        enemy.health -= 1       
                        if enemy.health <= 0:
                            enemy.kill()
                            if self.combo <= 29:
                                self.combo += 1
                                self.combo_bonus = self.combo * 10
                            self.score += (enemy.value + self.combo_bonus)
                    self.explosion_audio.play()  # Play explosion sound
                    laser.kill()

        # Enemy lasers
        if self.enemy_lasers:
            for laser in self.enemy_lasers:
                if pygame.sprite.spritecollide(laser, self.player, False):
                    self.player.sprite.health -= 1
                    self.combo = 0
                    self.combo_bonus = self.combo * 10
                    if self.player.sprite.health <= 0:
                        self.game_over = True  # Set game over state
                        self.handle_high_scores()
                    self.explosion_audio.play()  # Play explosion sound
                    self.damaged()
                    laser.kill()

        # Enemy collisions
        if self.enemies:
            for enemy in self.enemies:
                if pygame.sprite.spritecollide(enemy, self.player, False):
                    self.player.sprite.health -= 1
                    self.combo = 0
                    self.combo_bonus = self.combo * 10
                    if self.player.sprite.health <= 0:
                        self.game_over = True # Set game over state
                        self.handle_high_scores()  
                    self.explosion_audio.play()  # Play explosion sound
                    self.damaged()
                    enemy.kill()

    def display_score(self):
        score_surf = self.font.render(f'Score: {self.score}', False, 'white')
        score_rect = score_surf.get_rect(topleft=(10, 10))
        screen.blit(score_surf, score_rect)

    def display_lives(self):
        lives_surf = self.font.render(f'Lives: {self.player.sprite.health}', False, 'white')
        lives_rect = lives_surf.get_rect(topright=(screen_width - 10, 10))
        screen.blit(lives_surf, lives_rect)
    
    def display_combo(self):
        if self.combo > 0: 
            combo_surf = self.font.render(f'Combo: {self.combo}', False, 'white')
            combo_rect = combo_surf.get_rect(topleft=(10, 50))
            screen.blit(combo_surf, combo_rect)

    def display_game_over(self):
        
        pygame.mixer.music.stop()
        self.laser_audio.stop()
        self.explosion_audio.stop()
        
        screen.fill((0, 0, 0))

        # Display the game over message
        game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))
        score_text = self.font.render(f"Your Score: {self.score}", True, (255, 255, 255))
        restart_text = self.font.render("Restart", True, (255, 255, 255))
        quit_text = self.font.render("Quit", True, (255, 255, 255))

        # Center the text
        game_over_rect = game_over_text.get_rect(center=(screen_width / 2, screen_height / 4))
        score_rect = score_text.get_rect(center=(screen_width / 2, screen_height / 2))
        restart_rect = restart_text.get_rect(center=(screen_width / 2, screen_height / 1.5))
        quit_rect = quit_text.get_rect(center=(screen_width / 2, screen_height / 1.3))

        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)
        screen.blit(restart_text, restart_rect)
        screen.blit(quit_text, quit_rect)
       

        # Highlight selected option
        if self.selection == 0:
            restart_text = self.font.render("Restart", True, (255, 0, 0))  # Red color for selection
        
        else:
            quit_text = self.font.render("Quit", True, (255, 0, 0))  # Red color for selection

        screen.blit(restart_text, restart_rect)
        screen.blit(quit_text, quit_rect)

    def handle_high_scores(self):
        with open('records\\high_scores.txt', 'r') as file:
            current_scores = file.read()

        new_contents = str(self.score).zfill(10) + current_scores

        with open('records\\high_scores.txt', 'w') as file: 
            file.write(new_contents)

        os.system("code\\high_score")
        os.system("code\\move_to_hs")
    
    def handle_game_over_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:  # Move up
            if self.selection > 0:
                self.selection -= 1
        elif keys[pygame.K_DOWN]:  # Move down
            if self.selection < 1:
                self.selection += 1

        if keys[pygame.K_RETURN]:  # Enter key to select
            if self.selection == 0:
                self.reset_game()
                pygame.mixer.music.stop()
            elif self.selection == 1:
                pygame.quit()
                sys.exit()

    def reset_game(self):
        # Reset all variables to their initial states 
        player_sprite = Player((screen_width / 2, screen_height), screen_width, 8)
        self.player = pygame.sprite.GroupSingle(player_sprite)
        self.enemies.empty()
        self.enemy_lasers.empty()
        self.score = 0
        self.game_over = False
        self.selection = 0  # Reset selection to "Restart"

        # Restart the background music and SFX when the game restarts
        
        self.laser_audio.set_volume(0.1)  # Ensure laser audio is enabled again
        self.explosion_audio.set_volume(0.5)  # Ensure explosion audio is enabled again

    def pause_game(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE] and self.running == True:
            self.running = False
        if keys[pygame.K_RETURN] and self.running == False:
            self.running = True

    def display_pause_menu(self):
        screen.blit(self.pause_menu, (0, 0))
        pause_surf = self.maj_font.render("Paused", False, 'white')
        pause_rect = pause_surf.get_rect(center=(screen_width / 2, 200))

        return_surf = self.font.render("Enter = Unpause", False, 'white')
        return_rect = return_surf.get_rect(center=(screen_width / 2, 400))
        screen.blit(pause_surf, pause_rect)
        screen.blit(return_surf, return_rect)
    def run(self):
        # Check if game is getting paused
        self.pause_game()
        
        if self.game_over:
            self.display_game_over()
            self.handle_game_over_input()  # Handle user input on the game over screen
            return  # Stop the game logic

        # Update 
        # Is inside of an if-else because the game runs normally otherwise
        if self.running:
            # Spawn enemies
            self.spawn_enemy()
            self.spawn_enemy_reset()

            # Collision checking
            self.collision_check()
            self.player.update()
            self.enemies.update()
            self.enemy_lasers.update()
            self.increment_point_flag()
        else: 
            # Display pause menu 
            self.display_pause_menu()
            
        # Draw
        self.player.draw(screen)
        self.player.sprite.lasers.draw(screen)
        self.enemies.draw(screen)
        self.enemy_lasers.draw(screen)
        self.display_score()
        self.display_lives()
        self.display_combo()

# For extra graphics
class CRT:
  def __init__(self):
    self.tv = pygame.image.load('images\\tv.png').convert_alpha()
    self.tv = pygame.transform.scale(self.tv, (screen_width, screen_height))

  def create_lines(self):
    line_height = 3
    line_amount = int(screen_height/line_height)
    for line in range(line_amount):
      y_pos = line * line_height
      pygame.draw.line(self.tv,'black',(0, y_pos),(screen_width, y_pos), 1)

  def draw(self):
    self.tv.set_alpha(randint(75,90))
    self.create_lines()
    screen.blit(self.tv, (0,0))

# Main game loop
if __name__ == '__main__':
  pygame.init()
  screen_width = 400
  screen_height = 800

  screen = pygame.display.set_mode((screen_width, screen_height))
  clock = pygame.time.Clock()
  
  game = Game()
  crt = CRT()
  
  ENEMYLASER = pygame.USEREVENT + 1
  pygame.time.set_timer(ENEMYLASER, 2000)

  # Main loop
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      
      if event.type == ENEMYLASER:
        game.enemy_shoot()

    screen.fill((30,30,30))
    game.run()
    crt.draw()
    
    pygame.display.flip()
    clock.tick(game.tick)