from space import SpaceType

def stringify_flying_routes(routes):
  result = []
  for space in routes:
    result.append(space.make_pprint())

  if len(result) > 1:
    return '\n'.join(result)
  elif len(result) == 1:
    return result[0]
  else:
    return ''

class DroneFactory:
  def __init__(self):
    self.drone_id = 0

  def create_drone(self, starting):
    d_id = self.drone_id
    self.drone_id += 1
    return Drone(d_id, starting)

class Drone:
  def __init__(self, drone_id, init_block):
    self.drone_id = drone_id
    self.flying_route = [init_block]
    self.init_block = init_block

  def __repr__(self):
    #return 'Drone ID: {0}\n  flying routes'.format(self.drone_id) + stringify_flying_routes(self.flying_route)
    return 'Drone ID: {0} Route length:{1}'.format(self.drone_id, len(self.flying_route))

  def fly_to_goal(self, universe):
    is_done = False
    while not is_done:
      last_block = self.flying_route[-1]
      if last_block.space_type == SpaceType.GOAL:
        is_done = True
      else:
        next_block_address = last_block.next_one(universe)
        next_space = universe.spaces[next_block_address[0]][next_block_address[1]][next_block_address[2]]
        self.flying_route.append(next_space)

  def mutate(self, universe):
    self.flying_route = [self.init_block]
    self.fly_to_goal(universe)

  def get_i_in_flying_route(self, i):
    if i < 0 or i >= len(self.flying_route):
      return None
    return self.flying_route[i]
