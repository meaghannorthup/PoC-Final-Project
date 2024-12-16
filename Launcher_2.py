class Launcher:
  def __init__(self, term):
      self.term = term
      self.x = self.term.width // 2  # Center of the screen
      self.y = self.term.height -1  # At the bottom of the screen
      self.angle = 2  # Default diagonal launch direction

  def location(self):
    return self.x, self.y

  #def bounding_box(self):
    #return NotImplemented

  def move(self, direction):
    if direction == "LEFT" and self.x > 0: #Moves launcher to the left if it is within bounds
        self.x -= 1
    elif direction == "RIGHT" and self.x < self.term.width - 1: #Moves launcher to the right if it is within bounds
        self.x += 1 

  def set_angle(self, direction):
    if direction == "DOWN" and self.angle > 1:
        self.angle -= 1
    elif direction == "UP" and self.angle < 3:
        self.angle += 1  

  def respawn(self):
    #reset the ball to it's original location
    self.x = self.term.width // 2
    self.y = self.term.height -1
    self.angle = 2

  def __str__(self):
    # Determine the arrow character based on the angle
    if self.angle == 1:  # Diagonal up-right
        arrow = "↗"
    elif self.angle == 2:  # Straight up
        arrow = "↑"
    elif self.angle == 3:  # Diagonal up-left
        arrow = "↖"
    else:
        arrow = "↔"  # Default case
    return arrow
