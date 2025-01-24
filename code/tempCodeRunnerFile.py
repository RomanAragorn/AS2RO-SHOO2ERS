import pygame, sys
from player import Player
from laser import Laser
from timer import Timer
from boss import Boss
from boss_moves import Boss_move
from random import randint, choice

pygame.init()
display_width = 1920
display_height = 1080
screen_width = 400
screen_height = 800

display = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()
music = pygame.mixer.Sound('audio\\music.wav')

class Arcade:
    def __init__(self):
        self.arcade = pygame.image.load('images\\arcade.png').convert_alpha()
        self.arcade = pygame.transform.scale(self.arcade, (1920, 1080))

    def draw(self):
        display.blit(self.arcade, (0,0))

class Screen: 
    def __init__(self, screen_height, screen_width):
        self.screen = pygame.Surface((screen_width, screen_height))
        self.rect = self.screen.get_rect(center=(display_width/2, display_height - 438))
        self.screen.fill("red")
    def draw(self):
        display.blit(self.screen, self.rect)

boss = pygame.sprite.GroupSingle()
boss_summon = False

def summon_boss():
    global boss_summon
    boss_summon = True
    spawn_time = pygame.time.get_ticks()
    boss.add(Boss(100, spawn_time, has_drop=True))

def hello():
    print(pygame.time.get_ticks())
    print('hello')

arcade = Arcade()
screen = Screen(screen_height, screen_width)
player_sprite = Player((display_width/2, display_height - 50), display_width/2 + screen_width/2, 4)
player = pygame.sprite.GroupSingle(player_sprite)
boss_timer = Timer(2000, autostart = True, func = summon_boss)


while True: 
    for event in pygame.event.get():
        music.set_volume(1.0)
        music.play(loops=-1)
        if pygame.mixer.music.get_busy():
            print("Music is playing")
        else:
            print("Music is not playing")
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
                

    display.fill((30, 30, 30))
    
    player.draw(display)
    player.update()
    boss_timer.update()
    if boss:
        boss.draw(display)
        boss.update()
        boss.sprite.move_sprites.draw(display)
    arcade.draw()
    pygame.display.flip()
    clock.tick(60)