import pygame, sys
from player import Player
from laser import Laser

pygame.init()
screen_width = 400
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
# Spawn player
player_sprite = Player((screen_width / 2, screen_height), screen_width, 8)
player = pygame.sprite.GroupSingle(player_sprite)

# Shoots lasers in the middle
laser = Laser((screen_width / 2, 0), -4, screen_height) 
lasers = pygame.sprite.Group()
ENEMYLASER = pygame.USEREVENT + 1
pygame.time.set_timer(ENEMYLASER, 2000)

clock = pygame.time.Clock()

def invert_color():
    screen.fill((255, 0, 255))
    # inv = pygame.Surface((screen_height, screen_height))
    # inv.fill((255, 0, 255))
    # inv.blit(screen, (0,0), None, pygame.BLEND_RGBA_SUB)
    # screen.blit(inv, (0,0))

def collision_check():
    if lasers:
            for laser in lasers:
                if pygame.sprite.spritecollide(laser, player, False):
                    laser.kill()
                    invert_color()           

def run():
    player.draw(screen)
    lasers.add(laser)
    lasers.draw(screen)
    player.update()
    lasers.update()
    collision_check()




while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == ENEMYLASER:
            laser = Laser((screen_width / 2, 0), -4, screen_height)
            
    screen.fill((30, 30, 30))
    run()

    pygame.display.flip()
    clock.tick(60)