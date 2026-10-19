import pygame
from ml_racing.engine.ui.button import Button
import ml_racing.engine.screen as screen
from ml_racing.engine.ui.text import Text
from ml_racing.toolbar import Toolbar
from ml_racing.car import Car
from ml_racing.engine.input import Input
from ml_racing.constants import *
import json
import time

def _is_mouse_in_track():
  pos = Input.get_mouse_pos()
  return pos[1] <= TRACK_HEIGHT

class TrackBuilder:
  def __init__(self, go_back):
    self.go_back = go_back
    self.toolbar = Toolbar()

    self.redraw_btn = Button("Clear track", lambda: self.change_mode("DRAWING"))
    self.place_btn = Button("Place car/goal", lambda: self.change_mode("PLACING"))
    self.save_btn = Button("Save track", self.trigger_save)
    self.replay_btn = Button("Replay", lambda: self.replay_track())
    self.save_btn.disabled = True
    self.replay_btn.disabled = True

    track_size = (screen.SCREEN_SIZE[0], TRACK_HEIGHT)
    self.map_surf = pygame.Surface(track_size).convert_alpha()
    self.track_surf = pygame.Surface(track_size).convert_alpha()
    self.clear_map()

    self.show_buttons()

    screen.screen.event_handler.subscribe_event(pygame.KEYDOWN, self.type_track_name)

  def clear_and_go_back(self, modified = False):
    self.change_mode("DRAWING")
    self.track_name = ""
    self.go_back(modified)

  def show_buttons(self):
    self.toolbar.add_button_section("GoBack", [
      Button("Back", self.clear_and_go_back)
    ])
    
    self.toolbar.add_button_section("TrackBuilder", [
      self.redraw_btn,
      self.place_btn,
      self.save_btn,
      self.replay_btn
    ])

  def hide_buttons(self):
    self.toolbar.remove_button_section("TrackBuilder")

  def trigger_save(self):
    if self.mode != "SAVING": self.change_mode("SAVING")
    else: self.save()

  def save(self):
    self.draw_goal(self.map_surf)
    pygame.image.save(self.map_surf, f"tracks/{self.track_name}.png")
    with open(f"tracks/{self.track_name}.json", "w") as track_file:
      json.dump({
        "car_pos": [self.car_pos[0], self.car_pos[1]],
        "car_rotation": self.car_rot,
        "created_at": time.time()
      }, track_file)
    self.clear_and_go_back(modified=True)

    

  def type_track_name(self, event):
    if self.mode != "SAVING": return
    if event.key == pygame.K_BACKSPACE:
      self.track_name = self.track_name[:-1]
    else:
      self.track_name += event.unicode

    self.save_btn.disabled = self.track_name == ""

  def replay_track(self):
    self.car.speed = 0
    self.car.angular_speed = 0

    self.car.pos = self.car_pos.copy()
    self.car.rotation = self.car_rot

  def clear_map(self):
      self.current_stage = 0
      self.track_surf.fill((0,0,0,0))
      self.map_surf.fill(GRASS_COLOR)
      self.goal_pos = [None, None]
      self.car_pos = None
      self.car_rot = None

  def __del__(self):
    self.toolbar.remove_button_section("TrackBuilder")

  def change_mode(self, new_mode):
    self.mode = new_mode

    if self.mode == "DRAWING":
      self.clear_map()
      self.redraw_btn.set_str("Clear track")
      self.place_btn.set_str("Place car/goal")
      self.redraw_btn.disabled = False
      self.place_btn.disabled = False
      self.save_btn.disabled = True
      self.replay_btn.disabled = True
      self.dead = False
    elif self.mode == "PLACING":
      self.redraw_btn.set_str("Redraw track")
      self.place_btn.set_str("Place car/goal")
      self.place_btn.disabled = True
      self.save_btn.disabled = True
      self.replay_btn.disabled = True
      self.rotating_car = False
      self.car = Car(pygame.Vector2(screen.SCREEN_SIZE) / 2)
      self.goal_pos = [None, None]
      self.placing_mode = "CAR"
    elif self.mode == "DONE":
      self.redraw_btn.set_str("Redraw track")
      self.place_btn.set_str("Move car/goal")
      self.place_btn.disabled = False
      self.save_btn.disabled = False
      self.replay_btn.disabled = False
    else:
      self.replay_track()
      self.save_btn.set_str("Confirm save")
      self.redraw_btn.disabled = True
      self.place_btn.disabled = True
      self.save_btn.disabled = True
      self.replay_btn.disabled = True

    self.toolbar.reposition()

  def draw_track_point(self, pos):
    """ Draws a single point of the track """
    pygame.draw.circle(self.track_surf, TRACK_COLOR, pos, TRACK_SIZE / 2)
    pygame.draw.circle(self.map_surf, SIDE_COLOR, pos, TRACK_SIZE / 2 + SIDE_SIZE)

  def draw_track_segment(self, start_pos, end_pos):
    """ Draws a line segment of track """
    if end_pos is None:
      self.draw_track_point(start_pos)
    else:
      while (end_pos.distance_squared_to(start_pos) > 1):
        self.draw_track_point(end_pos)
        end_pos = end_pos.move_towards(start_pos, 1)

  def draw_goal(self, surf):
    if self.goal_pos[0] is not None: 
      if self.goal_pos[1] is not None:
        pygame.draw.line(surf, GOAL_COLOR, self.goal_pos[0], self.goal_pos[1], 5)
      else:
        pygame.draw.circle(surf, GOAL_COLOR, self.goal_pos[0], 5)

  def update_draw(self, surf):
    if Input.is_mouse_pressed() and _is_mouse_in_track():
      curr_pos = Input.get_mouse_pos()
      self.draw_track_segment(curr_pos, self.last_pos)
      self.last_pos = curr_pos
    else:
      self.last_pos = None

    if Input.is_key_pressed('c'):
      self.clear_map()

  def update_placing(self, surf):
    if not _is_mouse_in_track(): return

    mouse_pos = Input.get_mouse_pos()
    if self.placing_mode == "CAR":
      self.car.pos = mouse_pos.copy()
      self.car_pos = mouse_pos.copy()
      if Input.is_mouse_just_pressed(): self.placing_mode = "ROTATE"
    elif self.placing_mode == "ROTATE":
      self.car.rotate_to_face(mouse_pos)
      self.car_rot = self.car.rotation
      if Input.is_mouse_just_pressed(): self.placing_mode = "GOAL1"
    elif self.placing_mode == "GOAL1":
      self.goal_pos[0] = mouse_pos.copy()
      if Input.is_mouse_just_pressed(): self.placing_mode = "GOAL2"
    elif self.placing_mode == "GOAL2":
      self.goal_pos[1] = mouse_pos.copy()
      if Input.is_mouse_just_pressed(): self.change_mode("DONE")

  def run(self, surf, deltaTime):
    self.toolbar.draw(surf)

    if self.mode == "DRAWING":
      self.update_draw(surf)
      self.map_surf.blit(self.track_surf, (0,0))
      surf.blit(self.map_surf, (0,0))
    elif self.mode == "PLACING":
      self.update_placing(surf)
      surf.blit(self.map_surf, (0,0))
      self.car.draw(surf)
      self.draw_goal(surf)

      if self.placing_mode == "CAR":
        text = Text.render("Click to place car")
      elif self.placing_mode == "ROTATE":
        text = Text.render("Click again to set car rotation")
      elif self.placing_mode == "GOAL1":
        text = Text.render("Click to set the first point of the goal at the end of the track")
      elif self.placing_mode == "GOAL2":
        text = Text.render("Click to set the second point of the goal at the end of the track")
      surf.blit(text, (10, 10))
    elif self.mode == "DONE":
      surf.blit(self.map_surf, (0,0))
      self.draw_goal(surf)
      if not self.car.update(deltaTime, self.map_surf): self.replay_track()
      self.car.draw(surf)
    else:
      surf.blit(self.map_surf, (0,0))
      self.car.draw(surf)
      self.draw_goal(surf)
      text = Text.render(f"Type track name: {self.track_name}")
      surf.blit(text, (10, 10))


  mode = "DRAWING" # DRAWING / PLACING / DONE
  redraw_btn = None
  place_btn = None
  save_btn = None
  replay_btn = None

  placing_mode = "CAR"  # CAR / ROTATE / GOAL1 / GOAL2
  car = None

  track_surf = None

  # MAP DATA (what needs to be saved)
  map_surf = None
  car_pos = None
  car_rot = None
  goal_pos = [None, None]
  track_name = ""

  go_back = None