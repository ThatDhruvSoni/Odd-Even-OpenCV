import random

class MarkovChainAI:
    def __init__(self):
        # 5 by 5 matrix to represent transitions with 1 based indexing, from [1][1] to [5][5]
        self.transitions = [[0] * 5 for i in range(5)]
        self.last_move = None
    
    def update(self, current_move):

        # If the game has not just begun, we update the transition matrix
        if self.last_move is not None:
            self.transitions[self.last_move - 1][current_move - 1] += 1
        
        #If the last move is None, we do not do anything except update the last move
        self.last_move = current_move
    
    def predict_next_move(self):
        #If the game has just begun and there is no last_move, we return a random int
        if self.last_move is None:
            return random.randint(1, 5)

        # Getting the transition probabilities from the last user move
        row = self.transitions[self.last_move - 1]

        # If there is no history for this last move, we return a random integer
        if sum(row) == 0:
            return random.randint(1, 5)
        
        # Return the number with the highest transition probability 
        return row.index(max(row)) + 1
    
    def get_player_out(self):
        return self.predict_next_move()

    