import pygame

DEFAULT_CURSOR = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW)
HAND_CURSOR = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)

just_pressed = False

class Input:

  @staticmethod
  def reset():
    global just_pressed
    just_pressed = False

  @staticmethod
  def init(event_handler):
    event_handler.subscribe_event(pygame.MOUSEBUTTONDOWN, lambda _: Input.register_just_pressed())

  @staticmethod
  def register_just_pressed():
    global just_pressed
    just_pressed = True

  @staticmethod
  def get_mouse_pos():
    return pygame.Vector2(pygame.mouse.get_pos())

  @staticmethod
  def is_mouse_pressed(button = 0):
    return pygame.mouse.get_pressed()[button]
  
  @staticmethod
  def is_mouse_just_pressed():
    return just_pressed

  @staticmethod
  def is_key_pressed(key):
    return pygame.key.get_pressed()[ord(key)]

  @staticmethod
  def set_cursor(cursor):
    pygame.mouse.set_cursor(cursor)