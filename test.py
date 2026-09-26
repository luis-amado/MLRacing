import pygame
from pygame.locals import *
from car import Car
import numpy as np
import math

size = (1280, 720)
track_color = (0,0,0,255)
side_color = 0x666666
grass_color = 0x145c20

pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("")
clock = pygame.time.Clock()
running = True

track_surface = pygame.Surface(size).convert_alpha()
map_surface = pygame.Surface(size)

def clear_map():
  track_surface.fill((0,0,0,0))
  map_surface.fill(grass_color)
clear_map()

clicked = False
last_pos = None
track_size = 100
side_size = 20

font = pygame.font.SysFont("Arial", 20)

mode = "DRAWING"

car = Car()

def draw_track_segment(pos):
  pygame.draw.circle(track_surface, track_color, pos, track_size / 2)
  pygame.draw.circle(map_surface, side_color, pos, track_size / 2 + side_size)

def draw_track(pos, last_pos):
  if last_pos is None:
    draw_track_segment(pos)
  else:
    while (last_pos.distance_squared_to(curr_pos) > 1):
      draw_track_segment(last_pos)
      last_pos = last_pos.move_towards(curr_pos, 1)

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.KEYDOWN:
      if event.unicode == "1": mode = "DRAWING"
      elif event.unicode == "2": 
        map_surface.blit(track_surface, (0,0))
        mode = "PLACING_CAR"

  if mode == "DRAWING":
    if pygame.key.get_pressed()[ord('c')]:
      clear_map()

    if pygame.mouse.get_pressed()[0]:
      curr_pos = pygame.Vector2(pygame.mouse.get_pos())
      draw_track(curr_pos, last_pos)
      last_pos = curr_pos
    else:
      last_pos = None

    map_surface.blit(track_surface, (0,0))
    screen.blit(map_surface, (0,0))
  elif mode == "PLACING_CAR":
    car.speed = 0
    car.angular_speed = 0
    screen.blit(map_surface, (0,0))

    car.pos = pygame.mouse.get_pos()
    car.draw(screen)
    if pygame.mouse.get_pressed()[0]:
      mode = "ROTATING_CAR"

  elif mode == "ROTATING_CAR":
    screen.blit(map_surface, (0,0))

    if not pygame.mouse.get_pressed()[0]:
      mode = "CAR_PLACED"
    else:
      car.rotate_to_face(pygame.mouse.get_pos())
      car.draw(screen)

  elif mode == "CAR_PLACED":
    screen.blit(map_surface, (0,0))
    car.update()
    car.draw(screen)

  mode_text = font.render(mode, False, "white")
  screen.blit(mode_text, (10, 10))

  pygame.display.flip()

  clock.tick(120)

pygame.quit()