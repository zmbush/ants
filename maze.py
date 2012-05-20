import heapq
import random
import pygame
import sys
import gradient

UP, DOWN, LEFT, RIGHT = range(4)
class Cell:
  def __init__(self):
    self.walls = [True] * 4

  def __str__(self):
    if self.walls[UP]:
      if self.walls[DOWN]:
        if self.walls[LEFT]:
          if self.walls[RIGHT]:
            return "[ ]"
          else:
            return "[  "
        else:
          if self.walls[RIGHT]:
            return "  ]"
          else:
            return " = "
      else:
        if self.walls[LEFT]:
          if self.walls[RIGHT]:
            return "/ \\"
          else:
            return "/  "
        else:
          if self.walls[RIGHT]:
            return "  \\"
          else:
            return " - "
    else:
      if self.walls[DOWN]:
        if self.walls[LEFT]:
          if self.walls[RIGHT]:
            return "\\ /"
          else:
            return "\\  "
        else:
          if self.walls[RIGHT]:
            return "  /"
          else:
            return " _ "
      else:
        if self.walls[LEFT]:
          if self.walls[RIGHT]:
            return "| |"
          else:
            return "|  "
        else:
          if self.walls[RIGHT]:
            return "  |"
          else:
            return "   "


def getDir(start, end):
  if start[0] == end[0]:
    if start[1] < end[1]:
      return RIGHT
    else:
      return LEFT
  elif start[1] == end[1]:
    if start[0] < end[0]:
      return DOWN
    else:
      return UP
  raise "Invalid Move"

def flip(d):
  if d == UP:
    return DOWN
  elif d == DOWN:
    return UP
  elif d == LEFT:
    return RIGHT
  else:
    return LEFT

def getChildren(pos):
  retval = []
  if pos[0] - 1 >= 0:
    retval.append((pos[0] - 1, pos[1]))
  if pos[1] - 1 >= 0:
    retval.append((pos[0], pos[1] - 1))
  if pos[0] + 1 < dim:
    retval.append((pos[0] + 1, pos[1]))
  if pos[1] + 1 < dim:
    retval.append((pos[0], pos[1] + 1))
  return retval

dim = 30
if len(sys.argv) > 1:
  dim = int(sys.argv[1])
sizemult = 700/dim
grid = []
for i in range(dim):
  grid.append([])
  for j in range(dim):
    grid[i].append(Cell())


heap = []
start = (0, 0)
end = (dim-1, dim-1)
for successor in getChildren(start):
  heapq.heappush(heap, (random.random(), start, successor))


white = (255, 255, 255)
black = (0, 0, 0)
def redrawGrid(grid, window, closedlist):
  window.fill(white)

  for y in range(len(grid)):
    for x in range(len(grid[y])):
      if (y, x) in closedlist:
        item = grid[y][x]
        #if item.walls[UP]:
        #  pygame.draw.line(window, black, (x*sizemult, y*sizemult), (x*sizemult+sizemult, y*sizemult))
        if item.walls[DOWN]:
          pygame.draw.line(window, black, (x*sizemult, y*sizemult+sizemult), (x*sizemult+sizemult, y*sizemult+sizemult))
        #if item.walls[LEFT]:
        #  pygame.draw.line(window, black, (x*sizemult, y*sizemult), (x*sizemult, y*sizemult+sizemult))
        if item.walls[RIGHT]:
          pygame.draw.line(window, black, (x*sizemult+sizemult, y*sizemult), (x*sizemult+sizemult, y*sizemult+sizemult))
  pygame.display.update()

def gridToPos(coord, scale):
  return (coord[1]*scale + scale/2, coord[0]*scale + scale/2)

closedlist = [start]

display = 0
while len(heap) > 0:
  value = heapq.heappop(heap)
  percentage = (float(len(closedlist)) / (dim*dim)) * 100
  if int(percentage) % 10 == 0 and display < int(percentage):
    display = percentage
    print "%s%% complete" % percentage
  if value[2] not in closedlist:

    a = grid[value[1][0]][value[1][1]]
    b = grid[value[2][0]][value[2][1]]
    direction = getDir(value[1], value[2])
    a.walls[direction] = False
    b.walls[flip(direction)] = False
    closedlist.append(value[2])

    for child in getChildren(value[2]):
      if child not in closedlist:
        heapq.heappush(heap, (random.random(), value[2], child))

pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((sizemult*dim, sizemult*dim))
pygame.display.set_caption("boo")

pygame.draw.line(window, (255,255,255), (0, 0), (0, sizemult))

position = (0, 0)

redrawGrid(grid, window, closedlist)
pygame.draw.circle(window, (0, 0, 255), (position[1]*sizemult+sizemult/2,
                   position[0]*sizemult+sizemult/2), sizemult/4)
pygame.display.update()

def getMoves(pos, grid):
  this = grid[pos[0]][pos[1]]

  retval = []

  if not this.walls[UP]:
    retval.append((pos[0] - 1, pos[1]))
  if not this.walls[LEFT]:
    retval.append((pos[0], pos[1] - 1))
  if not this.walls[DOWN]:
    retval.append((pos[0] + 1, pos[1]))
  if not this.walls[RIGHT]:
    retval.append((pos[0], pos[1] + 1))
  return retval

def distance(start, end):
  return abs(start[0] - end[0]) + abs(start[1] - end[1])

positions = [position]
paths = [position]
draw = []
while True:
  down = [False] * 4
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LEFT:
        down[LEFT] = True
      if event.key == pygame.K_RIGHT:
        down[RIGHT] = True
      if event.key == pygame.K_UP:
        down[UP] = True
      if event.key == pygame.K_DOWN:
        down[DOWN] = True
    elif event.type == pygame.KEYUP:
      if event.key == pygame.K_LEFT:
        down[LEFT] = False
      if event.key == pygame.K_RIGHT:
        down[RIGHT] = False
      if event.key == pygame.K_UP:
        down[UP] = False
      if event.key == pygame.K_DOWN:
        down[DOWN] = False

  here = grid[position[0]][position[1]]
  moveMade = False
  bestMove = None
  bestDist = 0
  moves = sorted([(distance(pos, end), pos) for pos in getMoves(position,
                  grid)])
  print moves

  oldpos = position
  if down[LEFT]:
    if not grid[position[0]][position[1]].walls[LEFT]:
      position = (position[0], position[1] - 1)
  elif down[RIGHT]:
    if not grid[position[0]][position[1]].walls[RIGHT]:
      position = (position[0], position[1] + 1)
  elif down[UP]:
    if not grid[position[0]][position[1]].walls[UP]:
      position = (position[0] - 1, position[1])
  elif down[DOWN]:
    if not grid[position[0]][position[1]].walls[DOWN]:
      position = (position[0] + 1, position[1])

  if position == oldpos and position != end:
    for dist,move in moves:
      if move not in paths:
        if not moveMade:
          moveMade = True
          position = move
      else:
        pos = paths[::-1].index(move)
        if pos > bestDist:
          bestDist = pos
          bestMove = move
    if not moveMade:
      position = bestMove
  if position != oldpos:
    pygame.draw.circle(window, white, gridToPos(oldpos, sizemult), sizemult/4)
    if (oldpos, position) in draw:
      draw.remove((oldpos, position))
    if (position, oldpos) in draw:
      draw.remove((position, oldpos))
    draw.append((oldpos, position))

    paths.append(position)
    g = gradient.Gradient([
                              (255,255,255),
                              #(0, 0, 255),
                              #(0, 255, 0),
                              (255, 0, 0)
                          ])
    for i in range(len(draw)):
      perc = float(i) / len(draw)
      pygame.draw.line(window, g.getColor(perc), gridToPos(draw[i][0],
                       sizemult), gridToPos(draw[i][1], sizemult), 3)

    while position in positions:
      positions.pop()
    else:
      positions.append(position) 
    for i in range(len(positions) - 1):
      pygame.draw.line(window, (0, 255, 0), gridToPos(positions[i], sizemult),
                       gridToPos(positions[i+1], sizemult))

    pygame.draw.circle(window, (0, 0, 255), gridToPos(position,sizemult), 
                       sizemult/4) 
  if position == end:
    pygame.draw.circle(window, (0, 255, 255), gridToPos(position,sizemult), 
                       sizemult/4) 
  pygame.display.update()

  clock.tick(30)

