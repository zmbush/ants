import random
import pygame
import gradient

WALL, FOOD, AIR, ANTHILL = range(4)

def generateMap(size):
  retval = [[WALL]*size]
  noAnthill = True
  anthill = None
  for y in range(size - 2):
    retval.append([WALL])
    for x in range(size - 2):
      if random.random() < .7:
        retval[y+1].append(AIR)
      elif random.random() < .1:
        retval[y+1].append(FOOD)
      elif random.random() < .01 and noAnthill:
        retval[y+1].append(ANTHILL) 
        anthill = (x+1, y+1)
        noAnthill = False
      else:
        retval[y+1].append(WALL)
    retval[y+1].append(WALL)
  retval.append([WALL]*size)

  if noAnthill:
    anthill = (size/2, size/2)
    retval[size/2][size/2] = ANTHILL
  return (retval, anthill)

white = (255, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)
black = (0, 0, 0)
green = (0, 255, 0)
def drawMap(window, theMap, scale):
  window.fill(white)
  for y in range(len(theMap)):
    for x in range(len(theMap[y])):
      if theMap[y][x] == WALL: 
        window.fill(black, rect=pygame.Rect(x*scale, y*scale, scale, scale))

def drawFeatures(window, theMap, scale):
  for y in range(len(theMap)):
    for x in range(len(theMap[y])):
      if theMap[y][x] == ANTHILL:
        window.fill(yellow, rect=pygame.Rect(x*scale, y*scale, scale, scale))
      elif theMap[y][x] == FOOD:
        window.fill(red, rect=pygame.Rect(x*scale, y*scale, scale, scale))

def getSuccessors(theMap, p):
  retval = []
  if theMap[p[1]+1][p[0]] in (AIR, FOOD, ANTHILL):
    retval.append((p[0], p[1]+1))
  if theMap[p[1]-1][p[0]] in (AIR, FOOD, ANTHILL):
    retval.append((p[0], p[1]-1))
  if theMap[p[1]][p[0]+1] in (AIR, FOOD, ANTHILL):
    retval.append((p[0]+1, p[1]))
  if theMap[p[1]][p[0]-1] in (AIR, FOOD, ANTHILL):
    retval.append((p[0]-1, p[1]))
  return retval

if __name__ == "__main__":
  mapsize = 100
  scale = 5
  ants = 5
  theMap,anthill = generateMap(mapsize)

  print theMap

  pygame.init()
  clock = pygame.time.Clock()
  window = pygame.display.set_mode((mapsize*scale, mapsize*scale))
  pygame.display.set_caption("boo")

  position = anthill
  positions = [anthill] * ants
  leavingTrail = [True] * ants
  pheremones = [position]
  visited = [position]
  g = gradient.Gradient([ (255, 255, 255), (0, 0, 255) ])
  while True:
    print positions
    for p in range(ants):
      drawMap(window, theMap, scale)
      bestChild = None
      childDistance = -1
      suc = getSuccessors(theMap, positions[p])
      random.shuffle(suc)
      for child in suc:
        if child not in pheremones:
          bestChild = child
          childDistance = 99999999999
          break
        else:
          dist = pheremones[::-1].index(child)
          if dist > childDistance:
            childDistance = dist
            bestChild = child
      positions[p] = bestChild
      if theMap[positions[p][1]][positions[p][0]] == FOOD:
        leavingTrail[p] = True
      if leavingTrail[p]:
        while positions[p] in pheremones:
          pheremones.remove(positions[p])
        pheremones.append(positions[p])
          
      for i in range(len(pheremones)):
        perc = float(i) / len(pheremones)
        color = g.getColor(perc)
        pos = pheremones[i]
        window.fill(color, rect=(pos[0]*scale, pos[1]*scale, scale, scale))
      drawFeatures(window, theMap, scale)
      for ant in range(ants):
        pygame.draw.circle(window, green, (positions[ant][0]*scale + scale/2,
                                           positions[ant][1]*scale+scale/2), 2)
    pygame.display.update()
    clock.tick(30)
