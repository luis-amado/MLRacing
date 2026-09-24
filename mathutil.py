import math

def rotate_point(origin, point, angle):
  ox, oy = origin
  px, py = point

  qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
  qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
  return qx, qy

def keyMapTo1(keyMap, key):
  if keyMap[ord(key)]: return 1
  else: return 0

def moveTowards(current, target, distance):
  if target - current > 0.0:
    return min(current + abs(distance), target)
  else:
    return max(current - abs(distance), target)

def diffSign(a, b):
  return a > 0 and b < 0 or a < 0 and b > 0