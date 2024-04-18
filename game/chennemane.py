import time


class Chennemane:
    def __init__(self):
        # Initialize game board with 6 beads in each of the 14 pits
        self.board = [4] * 14
        # Current index of the player (0/1) whose turn it is
        self.turn = 0
        self.scores = [0, 0]  # Scores for Player 1 and Player 2

    def get_possible_moves(self):
        # Calculates starting index based on whose turn it is (Player 1: 0-6, Player 2: 7-13)
        start_index = 7 * (self.turn)
        return [i for i in range(start_index, start_index + 7) if self.board[i] > 0]

    def make_move(self, move, update_board, after, on_complete):
        beads = self.board[move]
        self.board[move] = 0
        index = move

        def place_bead():
            nonlocal beads, index
            if beads == 0:
                # If last bead is placed
                index = self.get_next_index(index)
                wins = self.board[index]
                self.board[index] = 0
                self.scores[self.turn] += wins
                self.turn = 1 - self.turn  # Change turn after all beads are placed
                update_board()  # Final update after move is complete
                on_complete()
                return

            # Move to the next pit index anticlockwise
            index = self.get_next_index(index)
            self.board[index] += 1
            beads -= 1

            if self.board[index] == 4:
                self.scores[index // 7] += 4
                self.board[index] = 0

            if beads == 0:
                index = self.get_next_index(index)
                beads = self.board[index]
                self.board[index] = 0

            update_board()
            after(100, place_bead)  # Schedule next bead placement

        place_bead()  # Start placing beads

    def get_next_index(self, current_index):
        # Returns the next index in the circular list
        return (current_index + 1) % 14

    def game_over(self):
        # The game is over if all pits on one side are empty
        player1_side_empty = all(x == 0 for x in self.board[0:7])
        player2_side_empty = all(x == 0 for x in self.board[7:14])
        game_over = player1_side_empty or player2_side_empty
        if game_over:
            # Collect all remaining beads and add to the respective player's score
            self.scores[0] += sum(self.board[0:7])
            self.scores[1] += sum(self.board[7:14])
            self.board = [0] * 14  # Reset the board
            return True
        return False

    def get_winner(self):
        # Determine the winner based on scores
        if self.scores[0] > self.scores[1]:
            return 'Player 1 wins with score ' + str(self.scores[0])
        elif self.scores[1] > self.scores[0]:
            return 'Player 2 wins with score ' + str(self.scores[1])
        else:
            return 'Draw'
