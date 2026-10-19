import pygame
import ml_racing.engine.screen as screen

pygame.font.init()
FONT = pygame.font.SysFont("Arial", 20)

class Text:

  @staticmethod
  def render(str, color = "white"):
    return FONT.render(str, False, color)
  
  @staticmethod
  def size(str):
    return FONT.size(str)

  @staticmethod
  def blit_centered(text, height, surf = screen.screen.surf):
      surf.blit(text, ((screen.SCREEN_SIZE[0] - text.get_width()) // 2, height))
