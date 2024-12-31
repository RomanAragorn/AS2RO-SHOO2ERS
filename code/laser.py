import pygame

class Laser(pygame.sprite.Sprite):
  def __init__(self, pos, speed, y_constraint):
    super().__init__()
    self.image = pygame.Surface((4,10))
    self.image.fill('white')
    self.rect = self.image.get_rect(center = pos)
    self.mask = pygame.mask.from_surface(self.image)
    self.speed = speed
    self.y_constraint = y_constraint

  def constraint(self):
    if self.rect.y >= self.y_constraint + 20 or self.rect.y <= -20:
      self.kill()

  def update(self):
    self.rect.y -= self.speed
    self.constraint()