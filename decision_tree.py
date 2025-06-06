import random
from sklearn.tree import DecisionTreeClassifier
import pandas as pd

class DecisionTreeAI:
    def __init__(self):
        self.turn = 0
        self.move_history = []
        self.result_history = []
        self.dataset = []
        self.model = None
        self.retrain_frequency = 5
        self.last_prediction = random.randint(1, 5)


    def update(self, user_move):
        self.turn += 1
        self.move_history.append(user_move)

        if self.turn >= 3:
            self.dataset.append({"turn": self.turn - 1,
                                  "last_move": self.move_history[-2],
                                    "last_last_move": self.move_history[-3],
                                      "next_move": user_move})
                
        if len(self.dataset) >= 3 and self.turn % self.retrain_frequency == 0:
            df = pd.DataFrame(self.dataset)
            X = df[["turn", "last_move", "last_last_move"]]
            y = df["next_move"]

            self.model = DecisionTreeClassifier(max_depth=3)
            self.model.fit(X, y)
        

    def predict_next_move(self) -> int:
        if self.model is None or len(self.move_history) < 2:
            self.last_prediction = random.randint(1, 5)
        else:
            """
            features = [[
                self.turn,
                self.move_history[-1],
                self.move_history[-2]
            ]]
            """
            features = pd.DataFrame([{
                "turn": self.turn,
                "last_move": self.move_history[-1],
                "last_last_move": self.move_history[-2]
            }])

            self.last_prediction = self.model.predict(features)[0]
        return self.last_prediction


    def get_player_out(self) -> int:
        # Predict and store the AI move
        return self.predict_next_move()


