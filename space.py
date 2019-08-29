from enum import Enum
from random import randint


def check_bounds(input, upper, lower):
  for i in range(3):
    if input[i] >= upper[i]:
      return False
    elif input[i] < lower[i]:
      return False
  return True

class SpaceType(Enum):
  START = 'START'
  GOAL = 'GOAL'
  NORMAL = 'NORMAL'

class Space:
  def __init__(self, x, y, z, space_type = SpaceType.NORMAL):
    self.space_type = space_type
    self.x = x
    self.y = y
    self.z = z

  def __repr__(self):
    return 'Space: {0} {1} {2}'.format(self.x, self.y, self.z)

  def next_one(self, universe):
    is_done = False
    lower_limit = [0, 0, 0]
    upper_limit = [universe.x_size, universe.y_size, universe.z_size]
    current = []
    while not is_done:
      current = [self.x, self.y, self.z]
      i = randint(0, 2)
      operator = 1 if randint(0,1) == 1 else -1
      current[i] = current[i] + operator
      if check_bounds(current, upper_limit, lower_limit):
        is_done = True
    return current

  def next_one_only_increment(self, universe):
    is_done = False
    lower_limit = [0, 0, 0]
    upper_limit = [universe.x_size, universe.y_size, universe.z_size]
    current = []
    while not is_done:
      current = [self.x, self.y, self.z]
      i = randint(0, 2)
      current[i] = current[i] + 1
      if check_bounds(current, upper_limit, lower_limit):
        is_done = True
    return current


  def make_pprint(self):
    return '{0} {1} {2}'.format(self.x, self.y, self.z)
