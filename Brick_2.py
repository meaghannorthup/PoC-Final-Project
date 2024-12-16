class Brick:
  def __init__(self, x, y):
      self.x = x
      self.y = y
      self.value = 1

  def location(self):
    return NotImplemented

  def bounding_box(self):
    return NotImplemented

  def __str__(self):
    return NotImplemented

  def new_brick(term, brick):
    #generate the next brick
    loc, val = self.location, self.value
    while hit_vany([head] + worm, nibble_locations(loc, val)):
        loc = Location(x=randrange(1, term.width - 1),
                       y=randrange(1, term.height - 1))
        val = nibble.value + 1
    return Nibble(loc, val)



#Generate between one and eight bricks all in the same row with values between one and 
#Each round the bricks move down (eight bricks overall)
#8x8 screen above launcher
# If the bricks touch the ground, game is over