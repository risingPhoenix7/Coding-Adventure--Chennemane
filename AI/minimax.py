from game.chennemane import Chennemane
import time


class MinimaxAI:
    def __init__(self, game: Chennemane, player_position=1, difficulty=3):
        self.game = game
        self.player_position = player_position
        self.difficulty = difficulty
        self.depth = 10 if difficulty == 1 else difficulty-1

    def compute_move(self):
        print("Computing move...")
        # Minimax algorithm with alpha-beta pruning

        def minimax(state, depth, alpha, beta, maximizing_player):
            if depth == 0 or state.game_over():
                return state.evaluate(), None

            if maximizing_player:
                max_eval = float('-inf')
                best_move = None
                for move in state.get_possible_moves():
                    new_state = state.copy()
                    new_state.make_move(move, lambda: None,
                                        None, lambda: None)
                    eval, _ = minimax(new_state, depth - 1, alpha, beta, False)
                    if eval > max_eval:
                        max_eval = eval
                        best_move = move
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
                return max_eval, best_move
            else:
                min_eval = float('inf')
                best_move = None
                for move in state.get_possible_moves():
                    new_state = state.copy()
                    new_state.make_move(move, lambda: None,
                                        None, lambda: None)
                    eval, _ = minimax(new_state, depth - 1, alpha, beta, True)
                    if eval < min_eval:
                        min_eval = eval
                        best_move = move
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
                return min_eval, best_move

        # Initial call to minimax from the current state of the game
        # print the time to compute the move
        a = time.time()
        _, move = minimax(self.game, self.depth,
                          float(
                              '-inf'), float('inf'), not ((self.player_position == 1) ^ (self.difficulty == 1))
                          )
        b = time.time()
        print("Time to compute move in ms: ", (b - a) * 1000)
        return move
