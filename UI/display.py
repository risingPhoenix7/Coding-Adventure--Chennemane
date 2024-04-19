import tkinter as tk
from PIL import Image, ImageTk
from game.chennemane import Chennemane
from AI.minimax import MinimaxAI
import math
import random

gap_between_players=2000

class GameBoard(tk.Tk):
    def __init__(self, game: Chennemane, ai, ai0=None, board_image_path='board.png', bead_image_path='manjotti.png'):
        super().__init__()
        self.move_number = 0
        self.game = game
        self.ai = ai
        self.cols = 14  # 14 pits on the board
        self.bead_size = 20  # Default size of beads, can be scaled
        self.bead_image_path = bead_image_path
        self.bead_image = Image.open(self.bead_image_path).resize(
            (self.bead_size, self.bead_size))
        self.positions = self.calculate_positions()
        self.score_labels = self.create_score_labels()
        self.ai0 = ai0
        self.setup_GUI(board_image_path)
        if self.ai0 is not None:
            self.process_ai_0_move()
        # Create score labels for displaying scores

    def calculate_positions(self):
        # Calculate positions for a single row of 14 pits
        positions = [0] * 14
        start_x = 68
        start_y = 239
        dx = 109
        dy = -165  # Not used since we are using a single row

        for i in range(7):
            positions[i] = (start_x + i * dx, start_y)  # Player 1's pits
            # Player 2's pits mirrored
            positions[13 - i] = (start_x + i * dx, start_y + dy)

        return positions

    def setup_GUI(self, board_image_path):
        self.canvas = tk.Canvas(self, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)

        # Load the board image
        self.board_image = Image.open(board_image_path)
        self.tk_board_image = ImageTk.PhotoImage(self.board_image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_board_image)

        # Setup initial bead images on the canvas
        self.bead_images = [[] for _ in range(self.cols)]
        self.update_board()
        self.status_label = tk.Label(
            self, text="Welcome to the Game!", font=('Helvetica', 16))
        self.status_label.pack()
        if self.ai0 is None:
            self.canvas.bind("<Button-1>", self.make_move_interactive)

    def update_board_with_delay(self):
        self.update_board()

    def update_board(self):
        self.canvas.delete("bead")  # Clear existing bead images
        for i in range(self.cols):
            bead_count = self.game.board[i]
            x, y = self.positions[i]
            self.bead_images[i] = self.visualize_beads(bead_count, x, y)
        self.update_scores()  # Update scores display after redrawing beads

    def visualize_beads(self, count, cx, cy):
        images = []
        if count == 0:
            return images  # No beads to display

        # Define bead positions based on the count
        if count > 10:
            radius = self.bead_size * 2.0
            angle = 2 * math.pi / 10  # Max out the circle at 10 beads visually
        else:
            radius = max(self.bead_size, (self.bead_size // 2) * count // 3)
            angle = 2 * math.pi / count

        positions = [(cx + radius * math.cos(i * angle), cy + radius *
                      math.sin(i * angle)) for i in range(min(count, 10))]

        for x, y in positions:
            img = ImageTk.PhotoImage(self.bead_image)
            image_id = self.canvas.create_image(
                x, y, image=img, anchor="center", tags="bead")
            # Save reference to avoid garbage collection
            images.append((img, image_id))

        # Overlay count text if beads are more than 7
        if count > 7:
            img_id = self.canvas.create_text(cx, cy, text=str(count), font=(
                'Arial', self.bead_size), fill="white", tags="bead")
            images.append(("text", img_id))

        return images

    def make_move_interactive(self, event):
        if self.game.turn == 1:
            print("Not your turn yet!")
            return
        closest_pit, min_distance = None, float('inf')
        for i in range(self.cols):
            x, y = self.positions[i]
            distance = ((x - event.x) ** 2 + (y - event.y) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                closest_pit = i
        if self.game.get_possible_moves() == []:
            self.end_game()

        elif closest_pit is not None and closest_pit in self.game.get_possible_moves():
            print(
                f"Move #: {self.move_number} : {len(self.game.get_possible_moves())}")
            self.move_number += 1
            self.canvas.delete("highlight")  # Clear previous highlights
            # Highlight the player's chosen pit
            self.highlight_pit(closest_pit, "blue")
            self.game.make_move(closest_pit, self.update_board_with_delay,
                                self.after, self.process_ai_move)
        else:
            print("Invalid move")

    def process_ai_0_move(self):
        self.status_label.config(text="Player 0's turn")
        # Wait for 2000 milliseconds (2 seconds) before continuing
        self.canvas.after(gap_between_players, self.execute_ai_0_move)

    def execute_ai_0_move(self):
        print(
            f"Move #: {self.move_number} : {len(self.game.get_possible_moves())}")
        self.move_number += 1
        if not self.game.game_over():
            self.canvas.delete("highlight")  # Clear previous highlights
            move = self.ai0.compute_move()  # Compute AI's move
            self.highlight_pit(move, "red")  # Highlight the AI's chosen pit
            self.game.make_move(
                move=move, update_board=self.update_board_with_delay, after=self.after, on_complete=self.process_ai_move)
            if self.game.game_over():
                self.end_game()
        else:
            self.end_game()

    def process_ai_move(self):
        self.status_label.config(text="Player 1's turn")
        # Wait for 2000 milliseconds (2 seconds) before continuing
        self.canvas.after(gap_between_players, self.execute_ai_move)

    def execute_ai_move(self):
        print(
            f"Move #: {self.move_number} : {len(self.game.get_possible_moves())}")
        self.move_number += 1
        if not self.game.game_over():
            self.canvas.delete("highlight")  # Clear previous highlights
            move = self.ai.compute_move()  # Compute AI's move
            self.highlight_pit(move, "red")  # Highlight the AI's chosen pit
            on_complete = (lambda: self.status_label.config(
                text="Player 0's turn")) if (self.ai0 is None) else self.process_ai_0_move
            self.game.make_move(
                move, self.update_board_with_delay, self.after, on_complete=on_complete)
            if self.game.game_over():
                self.end_game()
        else:
            self.end_game()

    def highlight_pit(self, pit, color):
        x, y = self.positions[pit]
        radius = 50  # Radius for the highlight circle, adjust as necessary
        # Create a highlight with a specific tag ("highlight")
        self.canvas.create_oval(x-radius, y-radius, x+radius,
                                y+radius, outline=color, width=4, tags="highlight")

    def create_score_labels(self):

        player_score = tk.Label(
            self, text="Player 0 Score: 0", font=('Arial', 16), bg='white')
        player_score.pack(side="left", padx=20)
        # Create labels to display scores for AI (Player 1) and Human (Player 2)
        ai_score = tk.Label(self, text="Player 1 Score: 0",
                            font=('Arial', 16), bg='white')
        ai_score.pack(side="right", padx=20)

        return (player_score, ai_score)

    def update_scores(self):
        self.score_labels[0].config(
            text="Player 0 Score: " + str(self.game.scores[0]))
        self.score_labels[1].config(
            text="Player 1 Score: " + str(self.game.scores[1]))

    def end_game(self):
        # Display the winner
        winner = self.game.get_winner()
        self.status_label.config(text=winner)
        self.update_board()  # Update the board one last time
