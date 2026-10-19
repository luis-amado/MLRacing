import pygame
import ml_racing.engine.screen as screen
from ml_racing.engine.ui.button import Button
from ml_racing.engine.input import Input
from ml_racing.constants import *

class Toolbar:

  def __init__(self):
    self.button_sections = []

  def draw(self, screen_surf):
    pygame.draw.rect(screen_surf, "black", ((0, screen.SCREEN_SIZE[1] - TOOLBAR_HEIGHT), (screen.SCREEN_SIZE[0], TOOLBAR_HEIGHT)))

    for _, buttons in self.button_sections:
      for button in buttons:
        button.draw(screen_surf)

    if Input.is_mouse_just_pressed():
      for _, buttons in self.button_sections:
        for button in buttons:
          button.handle_click()

  def position_section(self, section_index: int):
    left = 0
    
    if section_index > 0:
      last_btn = self.button_sections[section_index-1][1][-1]
      left = last_btn.pos[0] + last_btn.get_width() + 30

    gap = 10
    toolbar_start = screen.SCREEN_SIZE[1] - TOOLBAR_HEIGHT

    for button in self.button_sections[section_index][1]:
      button.pos = pygame.Vector2(left + gap, toolbar_start + gap)
      left += button.get_width() + gap

  def reposition(self):
    for i in range(len(self.button_sections)):
      self.position_section(i)

  def add_button_section(self, key, buttons: list[Button]):
    self.button_sections.append((key, buttons))
    self.position_section(len(self.button_sections)-1)

  def remove_button_section(self, key):
    index = -1
    for i in range(len(self.button_sections)):
      if self.button_sections[i][0] == key:
        index = i
        break
    if index == -1: return
    self.button_sections.pop(index)

    while index < len(self.button_sections):
      self.position_section(index)
      index += 1

  button_sections: list[tuple[str, list[Button]]]