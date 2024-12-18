import json
import os

#JSON File for leaderboard
class Leaderboard:
    def __init__(self, file_path = "leaderboard.json"):
        self.file_path = file_path
        self.data = self.load_leaderboard()

    # Load the leaderboard data from a leaderboard.json file
    def load_leaderboard(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                try:
                    return json.load(file) # Load existing data
                except json.JSONDecodeError:
                    return {} # Return an empty dictionary if the file does not load
        return {} # Return empty dictionary if the file doesn't exist

    # Save the Leaderboard data back to the file
    def save_leaderboard(self):
        with open(self.file_path, "w") as file:
            json.dump(self.data, file, indent = 4) # Write back the data with the right formatting
    
    # Add or update a player's score
    def update_score(self, player_name, score):
        # Ensure the score is updated only if it is higher
        self.data[player_name] = max(score, self.data.get(player_name, 0))
        self.save_leaderboard()  # Save updated data to file

    # Retrieve the leaderboard data
    def get_leaderboard(self):
        return sorted(self.data.items(), key=lambda x: x[1], reverse=True) # Sorts the scores in descending orders

    # Display the leaderboard in a readable format
    def display_leaderboard(self):
        leaderboard = self.get_leaderboard()
        print("\n--- Leaderboard ---")
        for rank, (player, score) in enumerate(leaderboard, start=1): # pulls the players rank, name, and top score
            print(f"{rank}. {player}: {score} points")
        print("\n Press escape to exit!")
