import pygame
from random import choice, randint
from timer import Timer
from boss_moves import Boss_move

class Boss(pygame.sprite.Sprite):
  def __init__(self, y_constraint, spawn_time, has_drop, arcade_screen_left=760, arcade_screen_right=1160, layer=3):
    super().__init__()
    self.image = pygame.image.load('images\\boss.png').convert_alpha()
    self.image = pygame.transform.scale(self.image, (200, 200))
    self.rect = self.image.get_rect(center = (960, 300))
    self.y_constraint = y_constraint
    self.spawn_time = spawn_time
    self.health_scaling = round(self.spawn_time / 500)
    self.has_drop = has_drop
    self.layer = layer
    self.health = 1000
    self.value = 5000
    self.left_constraint = arcade_screen_left
    self.right_constraint = arcade_screen_right
    self.move_sprites = pygame.sprite.Group()
    self.moves_list = []
    self.move_timer = Timer(5000, autostart=True, repeat=True, func=self.choose_move)

    self.moves = {
      'launch_fists': self.launch_fists,
      'fisteroid': self.fisteroid
      #'beam': '3'
    }

    for move in self.moves.values():
      self.moves_list.append(move)
    
  def go_down(self):
    if self.rect.y < 400: 
      self.rect.y += 3

  def choose_move(self):
    choice(self.moves_list)()

  def launch_fists(self):
    print('launched')
    for i in range(5): 
      self.move_sprites.add(Boss_move((randint(self.left_constraint, self.right_constraint), 200), 1080, kind='launch_fist'))

  def fisteroid(self):
    self.move_sprites.add(Boss_move((randint(self.left_constraint, self.right_constraint), 200), 1080, kind='launch_fist'))
  
  def update(self):
    self.go_down()
    self.move_timer.update()
    self.move_sprites.update()