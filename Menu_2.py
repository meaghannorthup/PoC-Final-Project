class Menu:
    def __init__(self, term):
        self.term = term
        self.selected = 0  # Index of the currently selected menu option
        self.options = ["New Game", "Choose Name", "Leaderboard", "Exit"]  # Available menu options

    def move(self, keystroke):
        # Update the selected option based on user input
        if keystroke == "UP" and self.selected > 0:
            self.selected -= 1  # Move selection up
        elif keystroke == "DOWN" and self.selected < len(self.options) - 1:
            self.selected += 1  # Move selection down

    def select(self):
        # Return the currently selected option
        return self.options[self.selected]

    def __str__(self):
        # Generate a string version of the menu with the selected option highlighted
        menu_str = f""
        for i, option in enumerate(self.options):
            if i == self.selected:
                menu_str += f"{self.term.on_bright_blue}> {option}{self.term.normal}\n"  # Highlight the selected option
            else:
                menu_str += f" {option}\n"  # Regular formatting for other options
        return menu_str
