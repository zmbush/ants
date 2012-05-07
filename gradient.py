class Gradient:
  def __init__(self, colors):
    self.colors = colors

  def getColor(self, percentage):
    increment = 1.0 / (len(self.colors) - 1)
    current = 0
    i = 0
    while not (percentage >= current and percentage <= current+increment):
      current += increment
      i += 1
    normalized = percentage - current
    newPerc = normalized / increment

    red1, green1, blue1 = self.colors[i]
    red2, green2, blue2 = self.colors[i+1]

    dred = red2 - red1
    dgreen = green2 - green1
    dblue = blue2 - blue1

    nred = int(red1 + newPerc*dred)
    ngreen = int(green1 + newPerc*dgreen)
    nblue = int(blue1 + newPerc*dblue)

    newColor = (nred, ngreen, nblue)


    '''
    print "Selection:",i
    print "Current:",current
    print "Increment:",increment
    print "normalized:",normalized
    print "newPerc",newPerc
    print "New Color:",newColor
    '''

    return newColor

if __name__ == "__main__":
  g = Gradient([(255, 255, 255), (0, 0, 0), (255,255,255)])

  g.getColor(0)
  g.getColor(.1)
  g.getColor(.2)
  g.getColor(.3)
  g.getColor(.4)
  g.getColor(.5)
  g.getColor(.6)
  g.getColor(.7)
  g.getColor(.8)
  g.getColor(.9)
  g.getColor(1)

