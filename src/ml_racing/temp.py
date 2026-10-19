import pygame
from ml_racing.car import Car

size = (1280, 720)
track_color = (0,0,0,255)
side_color = (102, 102, 102)
grass_color = (20, 92, 32)
goal_color = (252, 194, 3)

FPS = 120

pygame.init()
screen = pygame.display.set_mode(size, flags=pygame.NOFRAME)
pygame.display.set_caption("")
clock = pygame.time.Clock()
running = True

track_surface = pygame.Surface(size).convert_alpha()
map_surface = pygame.Surface(size).convert_alpha()

def clear_map():
  track_surface.fill((0,0,0,0))
  map_surface.fill(grass_color)
clear_map()

last_pos = None
track_size = 100
side_size = 30

font = pygame.font.SysFont("Arial", 20)

mode = "DRAWING"

car = Car()
start_pos = (0,0)
start_rot = 0
goal_pos = (0,0)
deltaTime = 1/FPS

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
      elif event.unicode == "o":
        pygame.image.save(map_surface, "tracks/my_track.png")
      elif event.unicode == "w" and event.mod == 1024:
        pygame.quit()
        running = False
        break

  if not running: break

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

    car.pos = pygame.Vector2(pygame.mouse.get_pos())
    car.draw(screen)
    if pygame.mouse.get_pressed()[0]:
      start_pos = car.pos
      mode = "ROTATING_CAR"

  elif mode == "ROTATING_CAR":
    screen.blit(map_surface, (0,0))

    if not pygame.mouse.get_pressed()[0]:
      start_rot = car.rotation
      mode = "PLACING_GOAL"
    else:
      car.rotate_to_face(pygame.mouse.get_pos())
      car.draw(screen)
  elif mode == "PLACING_GOAL":
    screen.blit(map_surface, (0,0))

    pos = pygame.mouse.get_pos()
    pygame.draw.circle(screen, goal_color, pos, track_size / 4)
    if pygame.mouse.get_pressed()[0]:
      goal_pos = pos
      mode = "GOAL_PLACED"
      pygame.draw.circle(map_surface, goal_color, pos, track_size / 4)
    car.draw(screen)

  elif mode == "GOAL_PLACED":
    screen.blit(map_surface, (0,0))
    alive = car.update(deltaTime, map_surface)
    car.draw(screen)
    if not alive:
      mode = "DEAD"
  elif mode == "DEAD":
    screen.blit(map_surface, (0,0))

  mode_text = font.render(mode, False, "white")
  fps_test = font.render(f"{clock.get_fps():.0f} fps", False, "white")
  screen.blit(mode_text, (10, 10))
  screen.blit(fps_test, (10, 30))

  pygame.display.flip()

  deltaTime = clock.tick(FPS) / 1000

pygame.quit()