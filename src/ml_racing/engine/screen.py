import pygame
from ml_racing.engine.event_handler import EventHandler
from ml_racing.engine.input import Input
from ml_racing.engine.input import *

SCREEN_SIZE = (1280, 720)
FPS = 120

class Screen:

  def __init__(self):
    self.surf = pygame.display.set_mode(SCREEN_SIZE, flags=pygame.NOFRAME)
    self.clock = pygame.time.Clock()
    self.event_handler = EventHandler()

    self.event_handler.subscribe_event(pygame.QUIT, lambda _: self.quit())
    Input.init(self.event_handler)

  def __del__(self):
    pygame.quit()

  def quit(self):
    self.running = False

  def poll_events(self):
    self.event_handler.poll_events()
    Input.set_cursor(DEFAULT_CURSOR)

  def end_frame(self):
    pygame.display.flip()
    self.deltaTime = self.clock.tick(FPS) / 1000
    Input.reset()

  surf = None
  clock = None
  running = True
  deltaTime = 1 / FPS
  event_handler = None

screen = Screen()