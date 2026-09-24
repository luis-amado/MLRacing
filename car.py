import pygame
import mathutil
import math

class Car:
  def __init__(self, _pos = pygame.Vector2(0,0)):
    self.pos = _pos

  def get_rect(self):
    minX = self.pos[0] - self.width / 2
    maxX = self.pos[0] + self.width / 2
    minY = self.pos[1] - self.length / 2
    maxY = self.pos[1] + self.length / 2

    points = [ (minX, minY),
               (minX, maxY),
               (maxX, maxY),
               (maxX, minY) ]
    for i in range(len(points)):
      points[i] = mathutil.rotate_point(self.pos, points[i], self.rotation)
    return points

  def get_arrow(self):
    minX = self.pos[0] - self.width / 2
    maxX = self.pos[0] + self.width / 2
    minY = self.pos[1] - self.length / 2

    triangle_size = self.width / 4

    points = [ (minX + triangle_size, minY + triangle_size),
               (maxX - triangle_size, minY + triangle_size),
               (self.pos[0], minY)   ]
    for i in range(len(points)):
      points[i] = mathutil.rotate_point(self.pos, points[i], self.rotation)
    return points

  def draw(self, surface):
    rect = self.get_rect()
    arrow = self.get_arrow()
    pygame.draw.polygon(surface, "blue", rect)
    pygame.draw.polygon(surface, "red", arrow)

  def get_forward(self):
    return pygame.Vector2(math.sin(self.rotation), -math.cos(self.rotation))

  def update(self):
    deltaTime = 1/120

    top_speed = 300
    top_angular_speed = 200

    acceleration = 500
    angular_acceleration = 400

    keys = pygame.key.get_pressed()

    forward_input = (mathutil.keyMapTo1(keys, 'w') - mathutil.keyMapTo1(keys, 's')) * top_speed
    rotation_input = (mathutil.keyMapTo1(keys, 'd') - mathutil.keyMapTo1(keys, 'a')) * math.radians(top_angular_speed)

    deceleration_boost = 1
    if mathutil.diffSign(self.speed, forward_input):
      deceleration_boost = 2
    self.speed = mathutil.moveTowards(self.speed, forward_input, acceleration * deceleration_boost * deltaTime)
    angular_boost = 1
    if mathutil.diffSign(self.angular_speed, rotation_input):
      angular_boost = 8
    self.angular_speed = mathutil.moveTowards(self.angular_speed, rotation_input, math.radians(angular_acceleration) * deltaTime * angular_boost)

    self.pos += self.speed * deltaTime * self.get_forward()
    self.rotation += self.angular_speed * deltaTime



  def rotate_to_face(self, point):
    point = pygame.Vector2(point) - self.pos
    if point != (0,0):
      self.rotation = math.atan2(point[1], point[0]) + math.pi / 2

  pos = pygame.Vector2(0,0)
  speed = 0
  angular_speed = 0
  rotation = 0
  width = 14
  length = 21