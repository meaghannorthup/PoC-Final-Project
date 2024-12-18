# Import Packages
import asyncio # Helps game to run
import random # Generates random numbers
import json # Loads leaderboard
import os # Loads leaderboard

# Import other game objects and settings
from blessed import Terminal
from utils_2 import write
from Ball_2 import Ball
from Launcher_2 import Launcher
from Menu_2 import Menu
from Brick_2 import Brick
from Scoreboard_2 import Scoreboard
from leaderboard_2 import Leaderboard


# This function allows the game to render the game objects and the terminal
def draw(term, launcher, balls, bricks, scoreboard, fps: int = 24):
    # Clear the screen and set initial location
    with term.location():
        write(term.home)

    # Display the scoreboard at the top of the screen
    with term.location(0, 0):
        write(f"{getattr(term, scoreboard.color)}{str(scoreboard)}{term.normal}") # Pulls attributes, text and then resets the scoreboard to normal

    # Clear all previous ball positions
    for ball in balls:
        prev_x, prev_y = ball.prev_location() # Pulls the previous location of each ball
        # NOTE: STRUGGLES TO ERASE THE SECOND AND FOLLOWING BALLS IN A SERIES
        with term.location(prev_x, prev_y):
            print(" ", end="")  # Overwrite previous ball position with a space

    # Draw balls in their current positions
    for ball in balls:
        curr_x, curr_y = ball.location()
        with term.location(curr_x, curr_y):
            print(str(ball), end="")

    # Clear and redraw the launcher
    with term.location(*launcher.prev_location()):
        print(" ", end="")  # Clears previous launcher position
    with term.location(*launcher.location()):
        print(str(launcher), end="")

    # Draw bricks using their bounding box and colored_row
    for brick in bricks:
        top_left, _ = brick.bounding_box()
        for row in range(brick.height):  # Iterate through the brick's height
            with term.location(top_left[0], top_left[1] + row):
                if row == brick.height // 2:  # Center row contains the value
                    write(f"{getattr(term, brick.color)}{str(brick)}{term.normal}") # Pulls the brick color, the value, and then resets the terminal
                else:
                    write(brick.colored_row(term)) # Pulls the brick color without the value

# This async function creates the start menu
async def start_menu(term, fps: int = 24):
    # Display the start menu
    menu = Menu()
    previous_output = "" # This is used to prevent blinking

    with term.fullscreen(), term.hidden_cursor(), term.cbreak():
        while True:

            output = str(menu)

            # Only redraws if the output has changed
            if output != previous_output:
                print(term.home + term.clear + output)
                previous_output = output

            # Waits for user input
            key = await poll(term, fps=fps)  # Waits for the user to enter a key

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

# This async function creates a display of the leaderboard
async def Leaderboard_Display(term, fps: int = 24):
    leaderboard = Leaderboard()
    with term.fullscreen(), term.hidden_cursor(), term.cbreak():
        leaderboard.display_leaderboard()

        while True:
            # Waits for user input
            key = await poll(term, fps=fps)  # Waits for the user to enter a key

            if key == "ESCAPE":  # Escape to the main menu
                print("Returning to the main menu!")
                await asyncio.sleep(2)
                return

# This async function allows the user to enter their name
async def Enter_Name(term, fps: int = 24):
    # User is prompted to enter their name
    name = ""  # Placeholder for the name
    with term.fullscreen(), term.hidden_cursor(), term.cbreak():
        while True:

            print(term.home)
            print("Enter your name (press Enter to confirm, Esc to cancel):")
            print(f"Name: {name}")

            # Waits for user input
            key = await poll(term, fps=fps)

            if key == "ENTER":  # Confirm the name
                if name.strip():  # Ensure the name is not empty
                    print(f"Hello, {name}! Returning to the main menu...")
                    await asyncio.sleep(2)
                    return name # Returns name so that it can be added the game settings
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

# This async function tracks user input via the keyboard
async def poll(term, fps: int = 24):
    # Process user input
    key = term.inkey(timeout=1/fps)

    if key is None or key == "":
        key = ""

    elif key.upper() in ("W", "A", "S", "D", "H", "J", "K", "L"):
        key = key.upper()

    elif key.upper() in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        key = key.upper()

    elif key.upper() in "1234567890":
        key = key.upper()

    elif key.is_sequence:
        if key.name == "KEY_ESCAPE" or key.code == 361:
            key = "ESCAPE"
        elif key.name == "KEY_LEFT" or key.code == 260:
            key = "LEFT"
        elif key.name == "KEY_DOWN" or key.code == 258:
            key = "DOWN"
        elif key.name == "KEY_UP" or key.code == 259:
            key = "UP"
        elif key.name == "KEY_RIGHT" or key.code == 261:
            key = "RIGHT"
        elif key.name == "KEY_ENTER" or key.code == 343:
            key = "ENTER"
        elif key.name in ("KEY_BACKSPACE", "KEY_DELETE") or key.code in (263, 330):
            key = "BACKSPACE"

    return key

# This async function staggers when the balls are launches
async def staggered_ball_movement(balls, bricks, launch_delay, fps):
    for i, ball in enumerate(balls):
        if not ball.launched and not ball.dead: # If the ball has not been launched and it is not dead...
            ball.launched = True # The ball is read to be launched

        # Move all launched balls in the same loop
        for moving_ball in balls:
            if moving_ball.launched and not moving_ball.dead: # If ball is launched and not dead...
                moving_ball.move(bricks) # Move the balls

        await asyncio.sleep(1 / fps)  # Control the frame rate

# This async function starts the game
async def game(term, fps: int = 24):
    # Main game loop
    round = 1  # Tracks the current round
    scoreboard = Scoreboard(round, term, player_name) # Tracks stats about the game and displays them
    launcher = Launcher(term) # Moves the ball before it is launched and allows user to toggle directions roughly 45 degrees (135, 180, and 225)
    balls = [Ball(term.width // 2, term.height - 2, term)] # The balls for the game
    bricks = [] # This list will hold all of the generated bricks
    game_live = True # The ball is moving and all balls are within bounds means this is true
    leaderboard = Leaderboard() # This allows access to the leaderboard JSON file

    # Add a flag to indicate if the ball is moving
    ball_moving = False
    launch_delay = 0.25  # Delay time between ball launches

    with term.fullscreen(), term.hidden_cursor(), term.cbreak():
        # Create the first row of bricks
        bricks.extend(Brick.generate_bricks(term.width, term.height, round)) # Adds all the elements to the bricks list

        # Main game loop
        while game_live:
            key = await poll(term, fps=24)  # This waits for user input

            draw(term, launcher, balls, bricks, scoreboard)

            # Handle launcher and ball controls if no ball is moving
            if not ball_moving:
                if key == "UP":
                    launcher.set_angle("UP")
                    for ball in balls:
                        ball.ball_angle("UP")  # All balls adjust angle
                elif key == "DOWN":
                    launcher.set_angle("DOWN")
                    for ball in balls:
                        ball.ball_angle("DOWN")  # All balls adjust angle
                elif key == "LEFT":
                    launcher.move("LEFT")
                    for ball in balls:
                        ball.follow("LEFT")  # All balls follow the launcher
                elif key == "RIGHT":
                    launcher.move("RIGHT")
                    for ball in balls:
                        ball.follow("RIGHT")  # All balls follow the launcher
                elif key == "ENTER":
                    ball_moving = True  # Start the game, first ball launches following by the others by flipping the ball_moving flag
                elif key == "ESCAPE": # Allows the user to exit the game when the ball is not in motion
                    print("Exiting Game")
                    await asyncio.sleep(1)
                    break

            # Staggered ball launching
            if ball_moving:
                await staggered_ball_movement(balls, bricks, launch_delay, fps) # Launches the balls staggered

                key = await poll(term, fps=24)  # This waits for user input
                if key == "ESCAPE": # Allows the user to exit the game when the ball is in motion
                    print("Exiting Game")
                    break

                if all(ball.dead for ball in balls if ball.launched): # If all balls are dead, below the bottom of the terminal then the round ends
                    round += 1
                    print(term.clear)
                    scoreboard.update(round) # Updates the scoreboard to the new round
                    await asyncio.sleep(1)

                    # Moves row of bricks down and spawns a new row of bricks on top
                    for brick in bricks:
                        brick.move_down()
                    new_bricks = Brick.generate_bricks(term.width, term.height, round)
                    bricks.extend(new_bricks) # Adds new bricks to the list of bricks

                    # Add a new ball for the next round, a ball is added every round
                    new_ball = Ball(term.width // 2, term.height - 2, term)
                    balls.append(new_ball)

                    # Reset the ball and launcher back to their original positions
                    for ball in balls:
                        ball.launched = False
                        ball.respawn(launcher)
                    launcher.respawn()
                    ball_moving = False

                # End the game if bricks reach the bottom 8th of the terminal
                for brick in bricks:
                    if brick.y >= (term.height - term.height//8):
                        print(term.on_red + term.clear, end="")
                        with term.location(term.width // 2, term.height // 2):
                            print((f"GAME OVER!!").center(term.width))
                            print((f"{player_name}, you made it to round {round} and scored {round * 10} points!").center(term.width)) # Each round earns the user 10 points
                            print(("SORRY :(").center(term.width))

                        # Save results to the leaderboard
                        leaderboard.update_score(player_name, round * 10)

                        game_live = False # The game is no longer live
                        await asyncio.sleep(3)

# Allows the game to run!
if __name__ == "__main__":
    # Run the game with the start menu
    term = Terminal()
    player_name = "Guest"
    while True:  # Use a loop to keep coming back to the start menu
        option = asyncio.run(start_menu(term))
        if option == "New Game":
            asyncio.run(game(Terminal(), fps=24))
        elif option == "Choose Name":
            new_name = asyncio.run(Enter_Name(Terminal(), fps=24))
            if new_name:
                player_name = new_name  # Update the player name
        elif option == "Leaderboard":
            asyncio.run(Leaderboard_Display(Terminal(), fps=24))
        elif option is False:  # Exit the program
            print(term.home + term.clear + "Goodbye!")
            break