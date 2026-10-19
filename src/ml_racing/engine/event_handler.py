import pygame

suscribe_index = 0

class EventHandler:

  def __init__(self):
    self.handlers = {}

  def poll_events(self):
    for event in pygame.event.get():
      if event.type not in self.handlers: continue
      for handler in self.handlers[event.type]:
        handler(event)

  def subscribe_event(self, event_type, handler):
    if event_type not in self.handlers:
      self.handlers[event_type] = []
    self.handlers[event_type].append(handler)

  handlers = None