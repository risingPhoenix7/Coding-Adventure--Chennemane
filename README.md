# Chennemane Game - README

## Overview of Chennemane

**Chennemane** is a traditional board game widely played in parts of India. It involves a board, which features a 2x7 layout totaling 14 pits. The game version implemented here is known as "Bulena Perga". The objective is strategic distribution and collection of coins from these pits to maximize gains.

### Gameplay Mechanics

The game is played on a board with a 2x7 matrix of pits. Each pit starts with a predefined number of coins. Players take turns choosing a pit from their side of the board and distributing the coins in it anticlockwise. The key rules are:

- **Distribution:** Begin from a selected pit and distribute its coins one-by-one into subsequent pits anticlockwise.
- **Continuation:** If the last coin lands in an occupied pit, continue distributing from that pit. If it lands in an empty pit, the next turn begins.
- **Harvesting:** If at any point a pit reaches exactly four coins (a "Bule"), those coins are harvested, i.e., removed from the board to the player's store.
- **Winning Condition:** The game ends when all pits are empty. The player with the most coins in their store wins.

![chennemane](https://github.com/risingPhoenix7/Gamebot-Chennemane/assets/96655704/7d0640bc-fb3f-4495-a1c9-dfe8a77a6bed)

### Structure of the Codebase

The codebase is structured into three main directories:

- **/game:** Contains the game logic, including board setup, rules enforcement, and managing the game state.
- **/AI:** Hosts the artificial intelligence logic. Currently, a Minimax algorithm with alpha-beta pruning is implemented, capable of achieving search depths of up to 11.
- **/UI:** Manages the User Interface, allowing players to interact with the game visually and/or via command line inputs.

### AI Implementation

The AI uses a classic Minimax algorithm with dynamic depth and alpha-beta pruning to optimize performance:
- **Dynamic Depth Control:** Allows the AI to search deeper when fewer coins are left on the board.
- **Alpha-Beta Pruning:** Reduces the number of nodes evaluated by the Minimax algorithm, enhancing efficiency.

The AI can reach impressive depths, making strategic decisions based on possible future states of the board. Plans are underway to integrate reinforcement learning models, using policy gradient techniques as the next step for training more advanced AI models.

## Running the Game

To play Chennemane, follow these steps:

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Configure AI players (optional):
   In `main.py`, set up the AI players as needed. For example:
   ```python
   from AI.difficulty_bots import get_difficulty_bot

   ai1 = get_difficulty_bot(difficulty=12, game=game, player_position=1)
   ai0 = get_difficulty_bot(difficulty=13, game=game, player_position=0)
   ```

3. Run the game:
   ```
   python main.py
   ```

   Modify `main.py` to set the AI difficulty or to switch between human and AI players.

## Future Enhancements

The next phase of development includes:
- **Reinforcement Learning Models:** Implementing policy gradient models to train the AI using the decisions made during the Minimax phase as a base.
- **UI Improvements:** Enhancing user interaction capabilities for a more engaging game experience.

Feel free to contribute to the development or suggest improvements. Enjoy playing Chennemane!
