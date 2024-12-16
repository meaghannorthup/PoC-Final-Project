class Ball:
  def __init__(self, x , y, term, xdim = 0, ydim = -1):
    self.term = term
    self.angle = 2
    self.x = x
    self.y = y
    self.direction = [xdim, ydim]  # Ball starts moving diagonally as this is the set direction of the launcher

# [1, 0] Moving Up (1)
# [1, 1] Moving to the right (2)
# [-1, 1] Moving to the left (3)

  def location(self):
    return (self.x, self.y)

  def follow(self, direction):
    if direction == "LEFT" and self.x > 0: #Moves ball to the left if it is within bounds
        self.x -= 1
    elif direction == "RIGHT" and self.x < self.term.width - 1: #Moves ball to the right if it is within bounds
        self.x += 1 

  def ball_angle(self, direction):
    if direction == "DOWN" and self.angle > 1:
        self.angle -= 1
    elif direction == "UP" and self.angle < 3:
        self.angle += 1  
    if self.angle == 1:
      self.direction = [1, -1]
    elif self.angle == 2:
      self.direction = [0, -1]
    elif self.angle == 3:
      self.direction = [-1, -1]


  def move(self):

    self.x += self.direction[0]
    print(self.y)
    self.y += self.direction[1]
    print(self.y)

    # Handle bouncing off walls
    if self.y > self.term.height - 1: #shortened to fix bug
        self.direction[1] = -1
    elif self.y <= 0:
        self.direction[1] = 1

    if self.x > self.term.width - 1:
        self.direction[0] = -1
    elif self.x <= 0:
        self.direction[0] = 1

  def respawn(self, launcher):
    #reset the ball to it's original location
    self.x = self.term.width // 2
    self.y = launcher.location()[1] - 1
    self.direction = [0, 1] 
    self.angle = 2

  # character for the ball: 
  def __str__(self):
    return "■"
