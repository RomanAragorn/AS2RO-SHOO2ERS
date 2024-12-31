import pygame

class Boss_move(pygame.sprite.Sprite):
  def __init__(self, pos, y_constraint, kind='launch_fist'):
    super().__init__()
    self.kind = kind 
    if kind == 'launch_fist':
      self.image = pygame.image.load('images\\fist.png').convert_alpha()
      self.image = pygame.transform.scale(self.image, (100, 100))
      self.rect = self.image.get_rect(center=(pos))
      self.mask = pygame.mask.from_surface(self.image)
      self.speed = 4
      self.y_constraint = y_constraint

  def update(self):
    if self.kind == 'launch_fist':
      if self.rect.y <= self.y_constraint:
        self.rect.y += self.speed
      else: 
        self.kill()