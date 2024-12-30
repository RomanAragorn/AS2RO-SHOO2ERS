import pygame
from laser import Laser

class Player(pygame.sprite.Sprite):
  def __init__(self, pos, x_constraint, speed):
    super().__init__()
    self.image = pygame.image.load('images\player.png').convert_alpha() 
    self.rect = self.image.get_rect(midbottom = pos)
    self.x_constraint = x_constraint
    self.left_constraint =  pos[0] - 200
    self.speed = speed
    self.ready = True
    self.laser_time = 0
    self.point_flag = 0
    self.laser_cooldown = 600
    self.health = 3
    self.max_health = 4
    self.laser_sound = pygame.mixer.Sound('audio\laser.wav')
    self.laser_sound.set_volume(0)
    self.lasers = pygame.sprite.Group()
    
  def get_input(self):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
      self.rect.x -= self.speed
    elif keys[pygame.K_RIGHT]:
      self.rect.x += self.speed

  def constraint(self):
    if self.rect.left <= self.left_constraint: 
      self.rect.left = self.left_constraint
    elif self.rect.right >= self.x_constraint: 
      self.rect.right = self.x_constraint
  
  def recharge(self):
    if not self.ready:
      current_time = pygame.time.get_ticks()
      if  current_time - self.laser_time >= self.laser_cooldown: 
        self.ready = True
      
  def shoot(self):
    if self.ready:
      self.laser_sound.play()
      self.lasers.add(Laser(self.rect.center, 8, self.rect.bottom))
      self.ready = False 
      self.laser_time = pygame.time.get_ticks()

  def update(self):
    self.get_input()
    self.constraint()
    self.shoot()
    self.lasers.update()
    self.recharge()