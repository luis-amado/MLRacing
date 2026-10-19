import pygame
from ml_racing.engine.screen import screen
from ml_racing.engine.ui.button import Button
from ml_racing.track_builder import TrackBuilder
from ml_racing.track_runner import TrackRunner
from ml_racing.main_menu import MainMenu

def main():
  current_screen = "MAIN"

  def change_mode(new_mode, modified = False):
    nonlocal current_screen, main_menu
    current_screen = new_mode

    if modified:
      main_menu.load_tracks()
      main_menu.set_page(main_menu.max_page)

  def change_selected_track(new_track):
    nonlocal track_runner
    track_runner.set_track(new_track)

  main_menu = MainMenu(change_mode, change_selected_track)
  track_builder = TrackBuilder(lambda modified: change_mode("MAIN", modified))
  track_runner = TrackRunner(lambda: change_mode("MAIN"))

  while screen.running:
    screen.poll_events()
    if not screen.running: break
    
    screen.surf.fill("black")

    if current_screen == "MAIN":
      main_menu.run(screen.surf)
    elif current_screen == "BUILDER": 
      track_builder.run(screen.surf, screen.deltaTime)
    elif current_screen == "RUNNER": 
      track_runner.run(screen.surf, screen.deltaTime)
    
    screen.end_frame()

if __name__ == "__main__":
  main()