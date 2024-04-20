import numpy as np
import tensorflow as tf
from keras import layers, models, optimizers
from keras import models
import os


class PolicyGradient:
    def __init__(self, learning_rate=0.01, player_position=1):
        self.learning_rate = learning_rate
        # self.model = self.create_model()
        self.model = self.load_model("models\policy_gradient_player1_1000.h5" if player_position == 1 else
                                     "models\policy_gradient_player0_1000.h5")
        self.player_position = player_position

    def create_model(self):
        # Model architecture
        model = models.Sequential([
            # Input layer for the board state
            layers.Dense(128, activation='relu', input_shape=(14,)),
            # Hidden layer
            layers.Dense(128, activation='relu'),
            # Output layer for 7 possible moves
            layers.Dense(7, activation='softmax')
        ])
        optimizer = optimizers.Adam(learning_rate=self.learning_rate)
        model.compile(optimizer=optimizer,
                      loss='sparse_categorical_crossentropy')
        return model

    def compute_move(self, board):
        # Adjust the board based on the player position
        if self.player_position == 1:
            board = np.roll(board, -7)  # Shift board for Player 1
        probs = self.model.predict(board.reshape(1, 14))[
            0]  # Predict move probabilities

        # Filter invalid moves (mask out moves leading to empty pits)
        # Only the first 7 entries are relevant due to normalization
        valid_moves = np.where(board[:7] > 0)[0]
        mask = np.zeros(7)
        mask[valid_moves] = 1
        filtered_probs = probs * mask

        if filtered_probs.sum() == 0:
            # No valid moves have positive probabilities, choose randomly among the valid moves
            if len(valid_moves) > 0:  # Check if there is at least one valid move
                action = np.random.choice(valid_moves)
            else:
                # If no valid moves, this is a critical error, handle accordingly
                raise ValueError(
                    "No valid moves available. Check game logic and state.")
        else:
            # Normalize the probabilities
            filtered_probs /= filtered_probs.sum()  # Normalize the probabilities
            # Choose an action based on the filtered probabilities
            action = np.random.choice(7, p=filtered_probs)

        # Map back to actual board index
        actual_action = (action + 7 * self.player_position) % 14
        return actual_action

    def train_step(self, states, actions, rewards):
        self.model.train_on_batch(states, actions, sample_weight=rewards)

    def save_model(self, file_path):
        self.model.save(file_path)

    def load_model(self, file_path):
        print("Loading model from: ", file_path)
        if not os.path.exists(file_path):
            print(f"Error: The file {file_path} does not exist.")
            return None
        try:
            model = models.load_model(file_path)
            return model
        except Exception as e:
            print(f"An error occurred while loading the model: {str(e)}")
            return None
