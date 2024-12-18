import random

class Brick:
    def __init__(self, x, y, term_width, term_height, value=1):
        self.x = x  # X-coordinate of the brick's top-left corner
        self.y = y  # Y-coordinate of the brick's top-left corner
        self.value = value  # Value of the brick
        self.width = term_width // 8  # Each brick is 1/8th of the terminal width
        self.height = term_height // 8  # Brick is 1/8th of terminal height
        self.color = self.value_to_color(value)  # Assign a color based on the value

    def value_to_color(self, value):
        # Map each value range to a color (gradient based on rounds 1-30)
        color_gradient = [
            "on_blue",      # Round 1-3
            "on_cyan",      # Round 4-6
            "on_green",     # Round 7-9
            "on_yellow",    # Round 10-12
            "on_magenta",   # Round 13-15
            "on_red",       # Round 16-18
            "on_white",     # Round 19-21
            "on_black",     # Round 22-24
            "on_bright_red",# Round 25-27
            "on_bright_blue"# Round 28-30
        ]
        # Scale value to the index in the color_gradient based on rounds
        index = min((value - 1) // 3, len(color_gradient) - 1)
        return color_gradient[index]

    def location(self):
        # Return the top-left corner of the brick
        return [self.x, self.y]

    def bounding_box(self):
        # Return the top-left and bottom-right coordinates of the brick
        return (self.x, self.y), (self.x + self.width - 1, self.y + self.height - 1)

    def move_down(self):
        # Move the brick down by one row
        self.y += self.height

    def reduce_value(self):
        # Reduce the value of the brick
        self.value -= 1
        if self.value > 0:
            self.color = self.value_to_color(self.value)  # Update the color if the brick is not destroyed

    def is_destroyed(self):
        # Check if the brick is destroyed (value is less than or equal to 0)
        return self.value <= 0

    def __str__(self):
        # Display the value of the brick centered within its width
        return str(self.value).center(self.width)

    def colored_row(self, term):
        # Return a row of the brick filled with its color
        color = getattr(term, self.color)  # Use the background color
        reset = term.normal  # Reset the terminal style
        return f"{color}{' ' * self.width}{reset}"

    @staticmethod # A static method is a function within a class that doesn't depend on the instance or class itself
    def generate_bricks(term_width, term_height, round, min_bricks=1, max_bricks=8):
        # Generate bricks for the current round
        bricks = []
        scoreboard_height = term_height // 9  # Height reserved for the scoreboard
        y = scoreboard_height  # Bricks start below the scoreboard
        brick_width = term_width // 8  # Standard brick width
        num_slots = 8  # Number of slots available for bricks

        for i in range(num_slots):
            # Randomly decide whether to skip this slot
            if random.random() < 0.6:  # 60% chance to leave a gap, this can be adjusted
                continue

            x = i * brick_width  # Calculate the position of the brick
            value = random.randint(1, round)  # Assign a random value based on the round
            bricks.append(Brick(x, y, term_width, term_height, value))  # Add the brick to the list

        return bricks
