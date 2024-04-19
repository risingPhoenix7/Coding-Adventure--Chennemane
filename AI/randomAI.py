from game.chennemane import Chennemane
import random


class RandomAI:
    def __init__(self, game: Chennemane):
        self.game = game

    def compute_move(self):
        return random.choice(self.game.get_possible_moves())
