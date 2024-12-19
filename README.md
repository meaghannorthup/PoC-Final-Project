# PoC-Final-Project

## Overview
This project is a terminal-based game built using Python. The game includes several key features, such as a menu system, a scoreboard, a leaderboard, and gameplay mechanics involving a launcher, bricks, and balls.

## Features
- **Menu System**: Navigate options like starting a new game, choosing a player name, viewing the leaderboard, and exiting.
- **Dynamic Gameplay**: Players control a launcher and break bricks using a ball, with the difficulty increasing each round.
- **Scoreboard**: Tracks and displays the player’s progress, including their current score and round.
- **Leaderboard**: Stores and displays the top scores in the game using a JSON file.
- **Customizable Design**: Built with modular classes for easy extension and customization.

## Project Structure
- `Menu`: Handles the game’s main menu navigation.
- `Scoreboard`: Tracks and displays player scores and rounds.
- `Launcher`: Manages player controls and the ball’s launch direction.
- `Ball`: Implements ball movement and collision detection.
- `Brick`: Handles brick placement, destruction, and interaction with the ball.
- `Utils` : Special code provided by Dan
- `Leaderboard`: Writes and updates the scoreboard.

## How to Play
1. Run the game:
   ```bash
   python game_2.py
   ```
2. Use the arrow keys to navigate the menu and select options.
3. During gameplay:
   - Use **Left/Right Arrow Keys** to move the launcher.
   - Use **Up/Down Arrow Keys** to adjust the launch angle.
   - Press **Enter** to launch the ball.
   - Try to destroy all bricks and survive as long as possible!
