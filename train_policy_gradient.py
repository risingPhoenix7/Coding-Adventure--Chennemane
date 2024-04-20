import numpy as np
import logging
from AI.policy_gradient import PolicyGradient
from game.chennemane import Chennemane
import AI.difficulty_bots as difficulty_bots

# Set up basic configuration for logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def train_policy_gradients(ai0, ai1, num_games=1000, save_path='models/', validation_interval=10, num_validation_games=5):
    validation_results = []

    for i in range(num_games):
        game = Chennemane()
        states, actions, rewards = {0: [], 1: []}, {
            0: [], 1: []}, {0: [], 1: []}
        logging.info(f"Starting game {i + 1}/{num_games}")

        while not game.game_over():
            current_player = game.turn
            current_model = ai0 if current_player == 0 else ai1
            board_state = np.array(game.board)
            action = current_model.compute_move(board_state.copy())
            game.make_move(action, lambda: None, None, lambda: None)
            evaluate = game.evaluate()
            reward = (evaluate - (game.scores[0] if current_player ==
                      0 else game.scores[1])) * (-1)**current_player

            states[current_player].append(board_state)
            actions[current_player].append((action-7*current_player) % 14)
            rewards[current_player].append(reward)

        for player in [0, 1]:
            states_np = np.array(states[player])
            actions_np = np.array(actions[player], dtype=np.int32)
            rewards_np = np.array(rewards[player])
            model_to_train = ai0 if player == 0 else ai1
            model_to_train.train_step(states_np, actions_np, rewards_np)

        # Validate the models every `validation_interval` games
        if (i + 1) % validation_interval == 0:
            win_rate_0_as_p0, win_rate_1_as_p1 = validate_model(
                ai0, ai1, 5, num_validation_games)
            validation_results.append(
                (i + 1, win_rate_0_as_p0, win_rate_1_as_p1))
            logging.info(
                f"Validation results at game {i + 1}: ai0 as P0 = {win_rate_0_as_p0 * 100:.2f}%, ai1 as P1 = {win_rate_1_as_p1 * 100:.2f}%")

        # Save models periodically
        if (i + 1) % 100 == 0:
            ai0.save_model(f'{save_path}policy_gradient_player0_{i + 1}.h5')
            ai1.save_model(f'{save_path}policy_gradient_player1_{i + 1}.h5')
            logging.info(f"Models saved at game {i + 1}")


def validate_model(model0,model1, difficulty, num_games):

    wins_as_p0 = 0
    wins_as_p1 = 0
    for _ in range(num_games // 2):
        game = Chennemane()
        minimax_ai_1 = difficulty_bots.get_difficulty_bot(
            difficulty=difficulty, game=game, player_position=1)
        if play_game(model0, minimax_ai_1, player_position=0, game=game):
            wins_as_p0 += 1
        game = Chennemane()
        minimax_ai_0 = difficulty_bots.get_difficulty_bot(
            difficulty=difficulty, game=game, player_position=0)
        if play_game(minimax_ai_0, model1, player_position=1, game=game):
            wins_as_p1 += 1
    return wins_as_p0 / (num_games // 2), wins_as_p1 / (num_games // 2)


def play_game(player_one_ai, player_two_ai, player_position, game):
    while not game.game_over():
        if game.turn == 0:
            action = player_one_ai.compute_move(np.array(game.board))
        else:
            action = player_two_ai.compute_move(np.array(game.board))
        game.make_move(action, lambda: None, None, lambda: None)
    # Return True if the specified player AI wins
    return game.scores[player_position] > game.scores[1 - player_position]


# Example usage
ai0 = PolicyGradient(player_position=0)
ai1 = PolicyGradient(player_position=1)
train_policy_gradients(ai0, ai1)
