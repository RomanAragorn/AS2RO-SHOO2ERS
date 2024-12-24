import pygame

class Enemy(pygame.sprite.Sprite):
  def __init__(self, color, x, y_constraint, spawn_time):
    super().__init__()
    self.image = pygame.image.load(f'images\\{color}.png').convert_alpha()
    self.rect = self.image.get_rect(topleft = (x,-50))
    self.color = color
    self.y_constraint = y_constraint
    self.spawn_time = spawn_time
    self.health_scaling = round(self.spawn_time / 500)
    
    if self.color == 'pink':
      self.speed = 2
      self.value = 100
      self.health = 2 + self.health_scaling
    elif self.color == 'green':
      self.image = pygame.transform.scale(self.image, (100,100))
      self.rect = self.image.get_rect(topleft = (x,-100))
      self.speed = 1
      self.value = 500
      self.health = 5 + self.health_scaling
    else:
      self.speed = 5
      self.value = 300
      self.health = 1 + self.health_scaling

  def constraint(self):
    if self.rect.y >= self.y_constraint + 50:
      self.kill()

  def update(self):
    self.rect.y += self.speed
    self.constraint()