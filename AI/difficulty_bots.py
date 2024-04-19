from AI.minimax import MinimaxAI
from AI.randomAI import RandomAI


def get_difficulty_bot(difficulty, game, player_position):
    if difficulty == 1:
        return MinimaxAI(game, player_position, difficulty=1)
    elif difficulty == 2:
        return RandomAI(game)
    else:
        return MinimaxAI(game, player_position, difficulty=difficulty-1)
