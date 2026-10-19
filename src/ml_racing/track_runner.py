from ml_racing.main_menu import Track
from ml_racing.toolbar import Toolbar
from ml_racing.engine.ui.button import Button
from ml_racing.engine.ui.text import Text
from ml_racing.car import Car
import json

class TrackRunner:

  def __init__(self, go_back):
    self.toolbar = Toolbar()
    self.go_back = go_back
    self.car = Car()

    self.toolbar.add_button_section("GoBack", [
      Button("Back", self.clean_and_go_back)
    ])

    self.toolbar.add_button_section("TrackControls", [
      Button("Play", self.start_countdown)
    ])

  def start_countdown(self):
    self.reset_position()
    self.playing = True
    self.timer = -1

  def clean_and_go_back(self):
    self.go_back()

  def set_track(self, new_track: Track):
    self.track = new_track
    self.reset_position()

  def reset_position(self, died = False):
    self.car.pos = self.track.car_pos.copy()
    self.car.rotation = self.track.car_rot
    self.car.speed = 0
    self.car.angular_speed = 0
    self.playing = False
    self.timer = 0
    self.died = died
    self.won = False

  def run(self, screen_surf, delta_time):
    screen_surf.blit(self.track.map, (0,0))

    if self.playing:
      self.timer += delta_time
    if self.playing or self.won:
      timer_text = Text.render(f"{self.timer:.2f}s")
      Text.blit_centered(timer_text, 20)
    elif self.died:
      Text.blit_centered(self.died_text, 20)

    if self.playing and self.timer >= 0 and not self.car.update(delta_time, self.track.map): 
      self.reset_position(died=True)

    if self.playing and self.car.has_won(self.track.map):
      self.playing = False
      self.won = True
      if not self.track.best or self.timer < self.track.best:
        self.track.best = self.timer
        with open(f"tracks/{self.track.name}.json", "r") as json_file:
          track_obj = json.load(json_file)
          track_obj["best_time"] = self.track.best
        with open(f"tracks/{self.track.name}.json", "w") as json_file:
          json.dump(track_obj, json_file)

    if self.track.best is not None:
      best_text = Text.render(f"Best: {self.track.best:.2f}s")
      Text.blit_centered(best_text, 45)
    
    self.car.draw(screen_surf)
    self.toolbar.draw(screen_surf)

  track = None
  timer = 0
  playing = False
  died = False
  won = False
  died_text = Text.render("You died!")