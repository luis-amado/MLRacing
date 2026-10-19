from ml_racing.engine.ui.button import Button
from ml_racing.toolbar import Toolbar
import ml_racing.engine.screen as screen
from ml_racing.engine.input import Input, HAND_CURSOR
from ml_racing.engine.ui.text import Text
from ml_racing.constants import *
import pygame
from pathlib import Path
import json

class Track:
  name: str
  map: pygame.Surface
  small_map: pygame.Surface
  car_pos: pygame.Vector2
  car_rot: float
  created_at: float
  best: None | float

MINIATURE_SCALE = 0.28
MINIATURE_GAP = 40
MINIATURE_ROWS = 2
MINIATURE_COLS = 3
MINIATURE_WIDTH = screen.SCREEN_SIZE[0] * MINIATURE_SCALE
MINIATURE_HEIGHT = TRACK_HEIGHT * MINIATURE_SCALE
HORIZONTAL_PADDING = (screen.SCREEN_SIZE[0] - (MINIATURE_COLS * (MINIATURE_WIDTH + MINIATURE_GAP) - MINIATURE_GAP)) // 2
BUTTON_HORIZONTAL_PADDING = 20

class MainMenu:

  def __init__(self, change_mode, change_track):
    self.toolbar = Toolbar()
    self.change_mode = change_mode
    self.change_track = change_track

    self.toolbar.add_button_section("Modes", [
      Button("Create track", lambda: change_mode("BUILDER"))
    ])

    self.load_tracks()

    self.prev_page_btn = Button("<", lambda: self.move_page(-1))
    self.next_page_btn = Button(">", lambda: self.move_page(1))

    self.prev_page_btn.disabled = True
    self.next_page_btn.disabled = self.max_page == 0

    self.prev_page_btn.pos = pygame.Vector2(BUTTON_HORIZONTAL_PADDING, TRACK_HEIGHT / 2)
    self.next_page_btn.pos = pygame.Vector2(screen.SCREEN_SIZE[0] - BUTTON_HORIZONTAL_PADDING - self.next_page_btn.get_width(), TRACK_HEIGHT / 2)


  def load_tracks(self):
    self.tracks = []
    directory = Path("tracks/")
    for file in directory.rglob("*.json"):
      track = Track()
      track.name = str(file)[7:-5]
      with open(file, "r") as json_file:
        info = json.load(json_file)
        track.car_pos = pygame.Vector2(info["car_pos"][0], info["car_pos"][1])
        track.car_rot = info["car_rotation"]
        track.created_at = info["created_at"]
        track.best = info["best_time"] if "best_time" in info else None
      track.map = pygame.image.load(f"tracks/{track.name}.png").convert_alpha()
      track.small_map = pygame.transform.smoothscale_by(track.map, MINIATURE_SCALE)
      self.tracks.append(track)

    self.tracks.sort(key=lambda track: track.created_at)
    
    self.max_page = (len(self.tracks)-1) // (MINIATURE_COLS * MINIATURE_ROWS)
    self.page_text = Text.render(f"Page {self.page+1}/{self.max_page+1}")

  def run(self, screen_surf: pygame.Surface):
    self.toolbar.draw(screen_surf)

    if Input.is_mouse_just_pressed():
      self.prev_page_btn.handle_click()
      self.next_page_btn.handle_click()

    mouse_pos = Input.get_mouse_pos()
    hover_track = None

    for i, track in enumerate(self.tracks):
      if i // (MINIATURE_COLS * MINIATURE_ROWS) != self.page: continue
      i %= MINIATURE_COLS * MINIATURE_ROWS
      x = i % MINIATURE_COLS
      y = i // MINIATURE_COLS

      x_pos = x * (MINIATURE_WIDTH + MINIATURE_GAP) + HORIZONTAL_PADDING
      y_pos = y * (MINIATURE_HEIGHT + MINIATURE_GAP) + 140

      screen_surf.blit(track.small_map, (x_pos, y_pos))

      if mouse_pos[0] >= x_pos and mouse_pos[0] <= x_pos + MINIATURE_WIDTH and mouse_pos[1] >= y_pos and mouse_pos[1] <= y_pos + MINIATURE_HEIGHT:
        hover_track = track
        Input.set_cursor(HAND_CURSOR)

    self.prev_page_btn.draw(screen_surf)
    self.next_page_btn.draw(screen_surf)
    Text.blit_centered(self.page_text, TRACK_HEIGHT - 50)

    top_text = Text.render(f"Select a track")
    Text.blit_centered(top_text, 50)
    if hover_track is not None:
      hover_text = Text.render(hover_track.name)
      if hover_track.best is not None: hover_text = Text.render(f"{hover_track.name} (best: {hover_track.best:.2f}s)")
      Text.blit_centered(hover_text, 75)

      if Input.is_mouse_just_pressed():
        self.change_mode("RUNNER")
        self.change_track(hover_track)

  def set_page(self, new_page):
    self.page = new_page

    self.prev_page_btn.disabled = self.page == 0
    self.next_page_btn.disabled = self.page == self.max_page
    self.page_text = Text.render(f"Page {self.page+1}/{self.max_page+1}")

  def move_page(self, delta):
    self.set_page(self.page + delta)

  page = 0
  max_page = 0
  page_text = Text.render("Page 1/1")
  toolbar = None
  tracks: list[Track] = []