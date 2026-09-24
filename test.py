import pygame
from pygame.locals import *
from car import Car
import numpy as np

size = (1280, 720)

pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("")
clock = pygame.time.Clock()
running = True

track_pixels = pygame.Surface(size)
track_pixels.fill(0x666666)

clicked = False
last_pos = None
brush_size = 60

font = pygame.font.SysFont("Arial", 20)

mode = "DRAWING"

car = Car()

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.KEYDOWN:
      if event.unicode == "1": mode = "DRAWING"
      elif event.unicode == "2": 
        mode = "PLACING_CAR"
        # also convert map (add danger zone)

  if mode == "DRAWING":
    if pygame.key.get_pressed()[ord('c')]:
      track_pixels.fill(0x666666)

    if pygame.mouse.get_pressed()[0]:
      curr_pos = pygame.Vector2(pygame.mouse.get_pos())

      if last_pos is None:
        pygame.draw.circle(track_pixels, "black", curr_pos, brush_size)
      else:
        while (last_pos.distance_squared_to(curr_pos) > 2):
          pygame.draw.circle(track_pixels, "black", last_pos, brush_size)
          last_pos = last_pos.move_towards(curr_pos, 1)

      last_pos = curr_pos
    else:
      last_pos = None

    screen.blit(track_pixels, (0,0))
  elif mode == "PLACING_CAR":
    car.speed = 0
    car.angular_speed = 0
    screen.blit(track_pixels, (0,0))

    car.pos = pygame.mouse.get_pos()
    car.draw(screen)
    if pygame.mouse.get_pressed()[0]:
      mode = "ROTATING_CAR"

  elif mode == "ROTATING_CAR":
    screen.blit(track_pixels, (0,0))

    if not pygame.mouse.get_pressed()[0]:
      mode = "CAR_PLACED"
    car.rotate_to_face(pygame.mouse.get_pos())
    car.draw(screen)

  elif mode == "CAR_PLACED":
    screen.blit(track_pixels, (0,0))
    car.update()
    car.draw(screen)

  mode_text = font.render(mode, False, "white")
  screen.blit(mode_text, (10, 10))

  pygame.display.flip()

  clock.tick(120)

pygame.quit()