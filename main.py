from UI.display import GameBoard
from game.chennemane import Chennemane
from AI.minimax import MinimaxAI
import AI.difficulty_bots as difficulty_bots


def main():
    # Initialize game
    game = Chennemane()
    # difficulty of 1 makes the worst possible move
    # difficulty of 12 makes the best possible move
    ai = difficulty_bots.get_difficulty_bot(
        difficulty=12, game=game, player_position=1)
    ai0 = difficulty_bots.get_difficulty_bot(
        difficulty=13, game=game, player_position=0)

    # Initialize UI
    ui = GameBoard(game, ai, ai0)
    ui.mainloop()


if __name__ == "__main__":
    main()
