from collections import Counter
from space import Space, SpaceType
from drone import DroneFactory
from random import random, randrange
from math import floor

def create_spaces_2(x, y, z):
  spaces = []
  for _x in range(x):
    y_spaces = []
    for _y in range(y):
      z_spaces = []
      for _z in range(z):
        space = Space(_x, _y, _z)
        z_spaces.append(space)
      y_spaces.append(z_spaces)
    spaces.append(y_spaces)
  return spaces

def set_start_and_goal(spaces, starting_cube, goal_cube):
  spaces[starting_cube['x']][starting_cube['y']][starting_cube['z']].space_type = SpaceType.START
  spaces[goal_cube['x']][goal_cube['y']][goal_cube['z']].space_type = SpaceType.GOAL

def glue(src, dst, universe):
  current = src
  glues = []
  while True:
    if current == dst:
      return glues
    next_block_address = current.next_one(universe)
    next_space = universe.spaces[next_block_address[0]][next_block_address[1]][next_block_address[2]]
    current = next_space
    glues.append(next_space)

def crossover(p, q, alpha, universe):
  p_routes = p.flying_route
  q_routes = q.flying_route
  p_idx = floor(len(p_routes) * alpha)
  q_idx = floor(len(q_routes) * alpha)
  head = p_routes[0:p_idx]
  tail = q_routes[q_idx:]
  new_flying_route = head + glue(head[-1], tail[0], universe) + tail
  return new_flying_route

def crossover2(p, q, alpha, universe, num_drones):
  # this function creates a new set of drones
  # new_set = [top (alpha * num_drones) from p] + [top ((1-alpha) * num_drones) from q]
  p.sort(key=lambda drone: len(drone.flying_route))
  q.sort(key=lambda drone: len(drone.flying_route))
  x = floor(num_drones * alpha)
  new_set = p[0:x] + q[x:]
  return new_set

class Universe:
  def __init__(self, x, y, z, starting_cube, goal_cube, max_drone_per_box, p_c, p_m, alpha):
    self.x_size = x
    self.y_size = y
    self.z_size = z
    self.p_c = p_c
    self.p_m = p_m
    self.alpha = alpha
    self.max_drone_per_box = max_drone_per_box
    self.spaces = create_spaces_2(x, y, z)
    set_start_and_goal(self.spaces, starting_cube, goal_cube)
    self.drone_factory = DroneFactory()
    self.starting_cube = self.spaces[starting_cube['x']][starting_cube['y']][starting_cube['z']]
    self.goal_cube = self.spaces[goal_cube['x']][goal_cube['y']][goal_cube['z']]

  def reset(self):
    self.drones = []
    self.cost = 0
    self.num_collision = 0

  def init_drones(self, num_drones):
    for _ in range(num_drones):
      drone = self.drone_factory.create_drone(self.starting_cube)
      self.drones.append(drone)

  def gen_solutions(self):
    for drone in self.drones:
      drone.fly_to_goal(self)


  def gen_children(self, p, q):
    # p and q are Solution
    # therefore do q.drones or p.drones to get the entire drones

    # consider each drone to be each gene
    # then drone from p and q could do cross over
    # glueing is necessary in such case
    #  glueing is also random --> this makes each generation worse than the last one
    #                             to solve this problem, we implemented gen_children2
    # mutation is also done for each drone
    child = p if random() < 0.5 else q

    for i in range(len(child.drones)):
      if random() < self.p_c:
        p_drone = p.drones[i]
        q_drone = q.drones[i]
        child.drones[i].flying_route = crossover(p_drone, q_drone, self.alpha, self)

      if random() < self.p_m:
        child.drones[i].mutate(self)

    self.drones = child.drones


  def gen_children2(self, p, q, num_drones):
    child = p if random() < 0.5 else q

    if random() < self.p_c:
      child.drones = crossover2(p.drones, q.drones, self.alpha, self, num_drones)

    for i in range(len(child.drones)):
      if random() < self.p_m:
        child.drones[i].mutate(self)

    self.drones = child.drones


  def compute_score(self, collision_penalty):
    return self.cost + (self.num_collision * collision_penalty)

  def compute_cost_and_collision(self):
    max_route_length = 0
    for drone in self.drones:
      route_length = len(drone.flying_route)
      max_route_length = max(max_route_length, route_length)
      self.cost = self.cost + route_length

    for i in range(max_route_length):
      time_slice = [None] * len(self.drones)
      for x in range(len(self.drones)):
        drone = self.drones[x]
        time_slice[x] = drone.get_i_in_flying_route(i)
      counts = dict(Counter(time_slice))
      for k, v in counts.items():
        if k is not None and k.space_type == SpaceType.NORMAL and v > self.max_drone_per_box:
          self.num_collision += 1




