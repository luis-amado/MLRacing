import pygame
from ml_racing.engine.ui.text import Text
from ml_racing.engine.input import Input
from ml_racing.engine.input import *
from ml_racing.engine.screen import screen

PADDING = 6

BG_COLOR = 0x0d1945
HOVER_BG_COLOR = 0x1d2857
DISABLED_BG_COLOR = 0x4d4d4d

class Button:
  def __init__(self, _str, _action, _pos = None):
    self.str = _str
    self.text = Text.render(_str)
    self.pos = _pos
    self.action = _action

  def set_str(self, new_str):
    self.str = new_str
    self.text = Text.render(new_str)

  def get_width(self):
    return Text.size(self.str)[0] + PADDING * 2

  def get_rect(self):
    text_size = Text.size(self.str)
    tl = self.pos
    dimensions = (text_size[0] + PADDING * 2, text_size[1] + PADDING * 2)
    return (tl, dimensions)

  def handle_click(self):
    if self.disabled: return
    if self.is_pos_inside(Input.get_mouse_pos()): self.action()
  
  def is_pos_inside(self, pos):
    rect = self.get_rect()
    tl = rect[0]
    br = rect[0] + rect[1]
    x, y = pos
    return x >= tl[0] and x <= br[0] and y >= tl[1] and y <= br[1]
  
  def draw(self, surf):
    if self.pos is None: return

    rect = self.get_rect()

    if self.disabled:
      pygame.draw.rect(surf, DISABLED_BG_COLOR, rect, 0, 5)

    elif self.is_pos_inside(Input.get_mouse_pos()):
      pygame.draw.rect(surf, HOVER_BG_COLOR, rect, 0, 5)
      Input.set_cursor(HAND_CURSOR)

    else: 
      pygame.draw.rect(surf, BG_COLOR, rect, 0, 5)

    surf.blit(self.text, self.pos + (PADDING, PADDING))

  str = None
  text = None
  pos: pygame.Vector2 = None
  action = None
  disabled = False