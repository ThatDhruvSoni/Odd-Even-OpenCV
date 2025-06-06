import random

"""
ai_choose() is a function that is used to get the AI's guess as to what the user will show
It randomly guesses a number between 1 and 5 to either score runs or get the user out
"""
def ai_choose():
    return random.randint(1, 5) # Randomly chooses a number between 1 and 5 and returns it


"""
play_round() is a function that is used to play a round of the game
It has 2 parameters:
    - player_move: The number the user displays
    - ai_move: The number the AI chooses
The function returns the output of playing the round as a tuple containing a string and a number
The string is displayed and the number is added to the total
"""
def play_round(player_move, ai_move):
    if player_move == ai_move: # Compares player and ai moves
        return ("OUT", 0) # Returns OUT, 0 if the moves match
    else:
        return ("SCORED", player_move) # Returns OUT 