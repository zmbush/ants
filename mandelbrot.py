"""

zn+1 = zn**2 + c


"""

import gradient
import pygame
import sys
import math

def escapeTime(c, iterations=100, threshold=4):
  """
    (a + bi) * (a + bi) = (a^2 + 2abi - b^2)
  """

  x = 0
  y = 0

  a,b = c
  iteration = 0
  while (x*x + y*y < threshold and iteration < iterations):
    iteration += 1

    x, y = x*x - y*y + a, 2*x*y + b

  return iteration

seen = {}
def continuousTime(c, iterations=100, threshold=4):
  """
    (a + bi) * (a + bi) = (a^2 + 2abi - b^2)
  """
  
  if c not in seen:
    x = 0
    y = 0

    a,b = c
    iteration = 0
    while (x*x + y*y < threshold and iteration < iterations):
      iteration += 1

      x, y = x*x - y*y + a, 2*x*y + b

    if (iteration >= iterations): 
      seen[c] = 0
      return 0
    else:
      return iteration - math.log(math.log(x*x + y*y) / math.log(threshold),2)
  return iterations



size = 200
pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((3*size, 2*size))
pygame.display.set_caption("Mandelbrot")

xmin = -2
xsize = 2
ymin = 1
ysize = -3
iterations = 100

def draw(xmin, xsize, ymin, ysize, window):
  g = gradient.Gradient([
                          (0, 0, 0),
                          (0, 255, 0),
                          (255, 0, 0),
                          (0, 0, 255),
                          (255, 255, 0),
                          (255, 255, 255)
                        ])
  for y in range(2*size):
    ypos = ymin + ((y / (3.0*size)) * ysize)
    for x in range(3*size):
      xpos = xmin + ((x / (2.0*size)) * xsize)
      perc = continuousTime((xpos, ypos), iterations=iterations,
                                      threshold=100) / float(iterations)
      color = g.getColor(perc)
      pygame.draw.line(window, color, (x, y), (x, y))
    pygame.display.update()

draw(xmin, xsize, ymin, ysize, window)

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    elif event.type == pygame.MOUSEBUTTONUP:
      mousex, mousey = event.pos
      if event.button == 1: # left click
        centerx = xmin + ((mousex / (2.0*size)) * xsize)
        centery = ymin + ((mousey / (3.0*size)) * ysize)
        ysize /= 2.0
        xsize /= 2.0
        xmin = centerx - (xsize/2)
        ymin = centery - (ysize/2)

        draw(xmin, xsize, ymin, ysize, window)

        iterations *= 1.001
