class Ball:
    def __init__(self, x, y, term, xdim=0, ydim=-1):
        self.term = term # The terminal!
        self.angle = 2  # Default angle of the ball
        self.x = x  # Current x-coordinate of the ball
        self.y = y  # Current y-coordinate of the ball
        self.prev_x = x  # Previous x-coordinate of the ball to stop trailing
        self.prev_y = y  # Previous y-coordinate of the ball to stop trailing
        self.direction = [xdim, ydim]  # This controls the angle of the ball
        self.launched = False  # Ball has not been launched yet
        self.dead = False  # Ball is not dead

    def launch(self):
        # Launch the ball if it has not been launched yet
        if not self.launched:
            self.launched = True

    def location(self):
        # Return the current location of the ball as a tuple
        return (self.x, self.y)

    def prev_location(self):
        # Return the previous location of the ball as a tuple
        return (self.prev_x, self.prev_y)

    def follow(self, direction):
        # Update the ball's location to follow the launcher
        self.prev_x, self.prev_y = self.x, self.y

        if direction == "LEFT" and self.x > 0:  # Moves ball to the left if it is within bounds
            self.x -= 1
        elif direction == "RIGHT" and self.x < self.term.width - 1:  # Moves ball to the right if it is within bounds
            self.x += 1

    def ball_angle(self, direction):
        # Adjust the angle of the ball based on user input
        if direction == "DOWN" and self.angle > 1:
            self.angle -= 1
        elif direction == "UP" and self.angle < 3:
            self.angle += 1
        
        if self.angle == 1:
            self.direction = [1, -1]  # Ball moves diagonally
        elif self.angle == 2:
            self.direction = [0, -1]  # Ball moves straight up
        elif self.angle == 3:
            self.direction = [-1, -1]  # Ball moves diagonally

    def move(self, bricks):
        # Move the ball if it has been launched
        if not self.launched:
            return

        # Save the previous location
        self.prev_x, self.prev_y = self.x, self.y

        # Move the ball if it is not dead
        if not self.dead:
            self.x += self.direction[0]
            self.y += self.direction[1]

            # Handle bouncing off walls
            if self.y <= 1:
                self.direction[1] = 1  # Reverse vertical direction

            if self.x > self.term.width - 1:
                self.direction[0] = -1  # Reverse horizontal direction
            elif self.x <= 0:
                self.direction[0] = 1  # Reverse horizontal direction

            # Check for collision with bricks
            for brick in bricks:
                top_left, bottom_right = brick.bounding_box()
                if top_left[0] <= self.x <= bottom_right[0] and top_left[1] <= self.y <= bottom_right[1]:
                    # Ball collided with a brick
                    brick.reduce_value()

                    # Adjust ball position to stay outside the brick
                    if self.direction[1] > 0:  # Ball moving downwards
                        self.y = top_left[1] - 1
                    elif self.direction[1] < 0:  # Ball moving upwards
                        self.y = bottom_right[1] + 1

                    if self.direction[0] > 0:  # Ball moving right
                        self.x = top_left[0] - 1
                    elif self.direction[0] < 0:  # Ball moving left
                        self.x = bottom_right[0] + 1

                    # Reverse vertical direction
                    self.direction[1] = -self.direction[1]

                    # Reduce brick value and remove if destroyed
                    if brick.is_destroyed():

                        # Clear the brick from the terminal immediately
                        for row in range(brick.height):
                            with self.term.location(brick.x, brick.y + row):
                                print(" " * brick.width, end="")

                        bricks.remove(brick)
                    break  # Exit after handling one collision

            # Stop ball if it goes off the screen
            if self.y >= self.term.height - 1:
                self.launched = False  # Stop the ball
                self.dead = True

    def respawn(self, launcher):
        # Reset the ball to its original location and defaults
        self.prev_x, self.prev_y = self.x, self.y
        self.x = self.term.width // 2  # Reset to the center horizontally
        self.y = self.term.height - 2  # Reset to near the bottom vertically
        self.angle = 2  # Reset angle to default
        self.direction = [0, -1]  # Reset to move straight up
        self.dead = False

    def __str__(self):
        # Character representation for the ball
        return "■"
