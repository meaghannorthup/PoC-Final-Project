class Scoreboard:
    def __init__(self, round, term, player_name):
        self.x = term.width // 2  # Center of the screen
        self.y = 1  # At the top of the screen
        self.width = term.width  # Full width of the terminal
        self.round = round  # Current round
        self.score = round * 10  # Score is calculated based on the round
        self.player_name = player_name  # Player's name
        self.color = "on_bright_cyan"  # Display color for the scoreboard

    def location(self):
        # Return the location of the scoreboard
        return [self.x, self.y]

    def __str__(self):
        # Display the scoreboard as a centered string
        return (f" PLAYER: {self.player_name} | ROUND: {self.round} | SCORE : {self.score}").center(self.width)

    def colored_row(self, term):
        # Returns a row filled with the scoreboard's background color
        color = getattr(term, self.color)  # Uses the background color attribute
        reset = term.normal  # Reset the terminal style
        return f"{color}{' ' * self.width}{reset}"

    def update(self, round):
        # Update the round and score on the scoreboard
        self.round = round
        self.score = round * 10
