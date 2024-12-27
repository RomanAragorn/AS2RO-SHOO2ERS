import pygame

class Drop(pygame.sprite.Sprite):
  def __init__(self, drop_type, y_constraint, pos):
    super().__init__()
    self.image = pygame.image.load(f'images\\{drop_type}.png').convert_alpha()
    self.image = pygame.transform.scale(self.image, (40, 40))
    self.rect = self.image.get_rect(center = pos)
    self.speed = 1
    self.type = drop_type
    self.y_constraint = y_constraint

  def constraint(self):
    if self.rect.y >= self.y_constraint + 50: 
      self.kill()

  def update(self):
    self.rect.y += self.speed
    self.constraint()