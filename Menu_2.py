class Menu:
  def __init__(self):
    self.selected = 0
    self.options = ["New Game", "Choose Name", "Leaderboard", "Exit"]

  def move(self, keystroke):
    if keystroke == "UP" and self.selected > 0:
      self.selected = self.selected - 1 # move up
    elif keystroke == "DOWN" and self.selected < 3:
      self.selected = self.selected + 1 # move down

  def select(self):
    return self.options[self.selected]

  def __str__(self):
    menu_str = ""
    for i, option in enumerate(self.options):
      if i == self.selected:
        menu_str += f"> {option}\n"  
      else:
        menu_str += f"  {option}\n"
    return menu_str
