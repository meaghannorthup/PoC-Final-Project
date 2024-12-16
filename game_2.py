from time import sleep
import asyncio

from blessed import Terminal

from utils_2 import write
from Ball_2 import Ball
from Launcher_2 import Launcher
from Menu_2 import Menu

# comment 
def draw(term, launcher, ball, fps: int = 24):
  with term.location():
    write(term.home + term.clear)

  #with term.location(term.width//2, term.height//2): #I don't understand the logic of this
    #draw(key)

  with term.location(*launcher.location()):
    write(str(launcher))

  with term.location(*ball.location()):
    write(str(ball))

  #Add bricks
  #Add food


def update(term, launcher, ball, fps: int = 24):
  launcher.move()
  launcher.set_angle()
  #Queue menu
  #Start game
  return

async def start_menu(term, fps: int = 24):
  menu = Menu()
  previous_output = ""

  with term.fullscreen(), term.hidden_cursor(), term.cbreak():
    while True:

      output = str(menu)

      # Only redraw if the output has changed
      if output != previous_output:
          print(term.home + term.clear + output)
          previous_output = output

      # Waits for user input
      key = await poll(term, fps=fps) #Changed to troubleshoot

      if key == "UP":
          menu.move("UP")
      elif key == "DOWN":
          menu.move("DOWN")
      elif key == "ENTER":
          selected_option = menu.select()
          if selected_option == "New Game":
              return "New Game"
          elif selected_option == "Choose Name":
              return "Choose Name"
          elif selected_option == "Leaderboard":
              return "Leaderboard"
          elif selected_option == "Exit":
              return False

async def Enter_Name(term, fps: int = 24):

  name = ""  # Name is at first the empty string
  with term.fullscreen(), term.hidden_cursor(), term.cbreak():
        while True:

            print(term.home + term.clear)
            print("Enter your name (press Enter to confirm, Esc to cancel):")
            print(f"Name: {name}")

            #Waits for user input
            key = await poll(term, fps=fps) # Chnaged to troubleshoot

            if key == "ENTER":  # Confirm the name
                if name.strip():  # Ensure the name is not empty
                    print(f"Hello, {name}! Returning to the main menu...")
                    await asyncio.sleep(2)
                    return
                else:
                    print("Name cannot be empty!")
                    await asyncio.sleep(1)
            elif key == "ESCAPE":  # Cancel input
                print("You loser, you didn't enter your name")
                await asyncio.sleep(2)
                return
            elif key in ("BACKSPACE", "DELETE"):  # Handle backspace
                name = name[:-1]  # Remove the last character
            else:
                name += key  # Add the typed character to the name


leaderboard = {} #Universal Leaderboard dictionary 

async def Leaderboard(term, fps: int = 24):

  with term.fullscreen(), term.hidden_cursor(), term.cbreak():
        while True:

          print(term.home + term.clear)
          print("Oop this game doesn't exist so sucks... press esc to go back")

          key = await poll(term, fps=fps) #Changed to troubleshoot

          if key == "ESCAPE":
            print("bye")
            await asyncio.sleep(2)
            return


# this processes user input
async def poll(term, fps: int = 24):
  key = term.inkey(timeout=1/fps)

  if key is None or key == "":
    key = ""

  elif key.upper() in ("W", "A", "S", "D", "H", "J", "K", "L"):
    key = key.upper()

  elif key.upper() in ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"):
    key = key.upper()

  elif key.upper() in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0"):
    key = key.upper()

  elif key.is_sequence:
    if key.name == "KEY_ESCAPE" or key.code == 361:
      key = "ESCAPE"
    elif key.name == "KEY_LEFT"  or key.code == 260:
      key = "LEFT"
    elif key.name == "KEY_DOWN"  or key.code == 258:
      key = "DOWN"
    elif key.name == "KEY_UP"    or key.code == 259:
      key = "UP"
    elif key.name == "KEY_RIGHT" or key.code == 261:
      key = "RIGHT"
    elif key.name == "KEY_ENTER" or key.code == 343:
      key = "ENTER"
    elif key.name in ("KEY_BACKSPACE", "KEY_DELETE") or key.code in (263, 330):
      key = "BACKSPACE"

  return key


async def game(term, fps: int = 24):
  launcher = Launcher(term)
  ball = Ball(term.width // 2, term.height - 2, term)
  
  # add a flag to indicate if the ball is moving
  ball_moving = False
  
  with term.fullscreen(), term.hidden_cursor(), term.cbreak():
    #print("Use LEFT and RIGHT arrows to control the launcher, \n and UP and DOWN to control the angle it launches from")
    #sleep(3)
    #print(term.home + term.clear + "Loading...get ready to lose")
    #sleep(2)

    #player = None
    #key = ""
    round = 1
    # main game loop
    while True:
      key = await poll(term, fps=24) # This fixes some of the problems with key entry

      draw(term, launcher, ball)

      #Use of keys if ball is not moving
      if not ball_moving:
          if key == "UP":
              launcher.set_angle("UP")
              ball.ball_angle("UP")
          elif key == "DOWN":
              launcher.set_angle("DOWN")
              ball.ball_angle("DOWN")
          elif key == "LEFT":
              launcher.move("LEFT")
              ball.follow("LEFT")
          elif key == "RIGHT":
              launcher.move("RIGHT")
              ball.follow("RIGHT")
          elif key == "ENTER":
              ball_moving = True
          elif key == "ESCAPE":
              print("Exiting Game")
              await asyncio.sleep(1)
              break

      # Move the ball if the flag switches
      if ball_moving:
        ball.move()

      #Handle when ball goes out-of-bounds
      if ball.y == term.height:
        print("YOU DIED... respawning")
        await asyncio.sleep(1)
        round +=1
        print(f"Welcome to round {round}")
        await asyncio.sleep(1)
        ball.respawn(launcher)
        launcher.respawn()
        ball_moving = False




# modify the framerate by changing `fps`
if __name__ == "__main__":

  term = Terminal()
  while True: #use a loop to keep coming back to the start menu

    option = asyncio.run(start_menu(term))
    if option == "New Game":
      asyncio.run(game(Terminal(), fps=24))
    elif option == "Choose Name":
      asyncio.run(Enter_Name(Terminal(), fps=24))
    elif option == "Leaderboard":
      asyncio.run(Leaderboard(Terminal(), fps=24))
      sleep(2)
    elif option is False:  # Exit the program
        print(term.home + term.clear + "Goodbye!")
        break



