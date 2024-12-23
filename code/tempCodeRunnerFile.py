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
score = 2000
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

def increment_point_flag():
    if player.sprite.point_flag <= 4:
        if score >= 100 and score < 500: 
            player.sprite.point_flag = 1
            player.sprite.laser_cooldown = 600 - (player.sprite.point_flag * 10)
        
        if score >= 500 and score < 1000:
            player.sprite.point_flag = 2
            player.sprite.laser_cooldown = 600 - (player.sprite.point_flag * 10)

        if score >= 1000 and score < 1500:
            player.sprite.point_flag = 3
            player.sprite.laser_cooldown = 600 - (player.sprite.point_flag * 10)

        if score >= 1500 and score < 2000:
            player.sprite.point_flag = 4
            player.sprite.laser_cooldown = 600 - (player.sprite.point_flag * 10)
        
        if score >= 2000:
            player.sprite.point_flag = 5
            player.sprite.laser_cooldown = 600 - (player.sprite.point_flag * 10)

def run():
    player.draw(screen)
    player.sprite.lasers.draw(screen)
    lasers.add(laser)
    lasers.draw(screen)
    player.update()
    lasers.update()
    collision_check()
    increment_point_flag()
    print(player.sprite.point_flag)


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