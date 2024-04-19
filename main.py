from UI.display import GameBoard
from game.chennemane import Chennemane
from AI.minimax import MinimaxAI


def main():
    # Initialize game
    game = Chennemane()
    ai = MinimaxAI(game, player_position=1, depth=10)

    # Initialize UI
    ui = GameBoard(game, ai)
    ui.mainloop()


if __name__ == "__main__":
    main()
