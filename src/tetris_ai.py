from tetris import Tetris, TetrisBoard
import copy
from settings import *
from main import Game
from agent import Agent
import numpy as np


class TetrisAI:
    def __init__(self, tetris):
        self.tetris = tetris
        self.tetris_board = TetrisBoard()

    def ai_move(self, x_pos):
        self.tetris.speed_up = True
        curr_piece = self.tetris.current_tetromino
        positions = [vec(x_pos, 0) + block.pos - INIT_POS_OFFSET for block in curr_piece.blocks]
        self.tetris_board.place_tetromino(curr_piece, positions)

    def ai_rotate(self, num_rotations):
        curr_piece = self.tetris.current_tetromino
        tetris_board_array = self.tetris.field_array
        for _ in range(num_rotations):
            self.tetris_board.rotate_block(curr_piece, tetris_board_array)

    def get_state_properties(self, board):
        return np.array(list(self.tetris_board.get_board_properties(board)))

    def get_next_states(self):
        states = {}
        piece_id = self.tetris.current_tetromino.type
        curr_piece = copy.deepcopy(self.tetris.current_tetromino)
        tetris_board_array = copy.deepcopy(self.tetris.field_array)

        if piece_id == 'O':
            num_rotations = 1
        elif piece_id in ["I", "S", "Z"]:
            num_rotations = 2
        else:
            num_rotations = 4

        for i in range(num_rotations):
            piece = copy.deepcopy(curr_piece)
            tetris_board_array_copy = copy.deepcopy(tetris_board_array)

            valid_xs = self.tetris.board_width
            for x in range(valid_xs + 1):
                positions = [vec(x, 0) + block.pos - INIT_POS_OFFSET for block in piece.blocks]
                if not self.tetris_board.is_collide(positions, tetris_board_array_copy):
                    self.tetris_board.place_tetromino(piece, positions)
                    while not piece.landing:
                        self.tetris_board.move_block_down(piece, tetris_board_array_copy)
                    self.tetris_board.add_tetromino_to_board(piece, tetris_board_array_copy)
                    states[(x, i)] = self.tetris_board.get_board_properties(tetris_board_array_copy)
                    # self.tetris_board.print_board(tetris_board_array_copy)

                    piece = copy.deepcopy(curr_piece)
                    tetris_board_array_copy = copy.deepcopy(tetris_board_array)
            self.tetris_board.rotate_block(curr_piece, tetris_board_array)
        return states

    def play_step(self, action):
        curr_piece = self.tetris.current_tetromino
        tetris_board_array = self.tetris.field_array

        x_pos, num_rotations = action
        reward = 0
        game_over = False

        self.ai_rotate(num_rotations)
        self.ai_move(x_pos)

        positions = [block.pos for block in curr_piece.blocks]
        if not self.tetris_board.is_collide(positions, tetris_board_array):
            self.tetris_board.place_tetromino(curr_piece, positions)
            while not curr_piece.landing:
                self.tetris_board.move_block_down(curr_piece, tetris_board_array)
        self.tetris.check_tetromino_landing()
        reward += self.tetris.num_lines ** 2 * WIDTH + 1
        self.tetris_board.clear_lines(tetris_board_array)
        self.tetris.sprite_group.update()

        if self.tetris.game_over:
            reward -= 5
            game_over = True
            if reward > 90:
                print("YO")

        return reward, game_over

    def reset(self):
        self.tetris.reset()
        return np.array([0, 0, 0, 0])

    def train(self, game):
        # Initialize training variable
        max_episode = 3000
        max_steps = 25000

        agent = Agent(4)

        episodes = []
        rewards = []

        current_max = 0

        for episode in range(max_episode):
            current_state = self.reset()
            done = False
            steps = 0
            total_reward = 0
            print("Running episode " + str(episode))

            while not done and steps < max_steps:
                # Render the board for visualization
                # game.check_events()
                # game.update()
                # Get all possible tetromino placement in current board
                next_states = self.get_next_states()

                # If the dict is empty, meaning game is over
                if not next_states:
                    break

                # Tell agent to choose the best possible state
                best_state = agent.act(next_states.values())

                # Grab best tetromino position and its rotation chosen by the agent
                best_action = None
                for action, state in next_states.items():
                    if best_state == state:
                        best_action = action
                        break

                reward, done = self.play_step(best_action)
                total_reward += reward

                game.check_events()
                game.draw()

                # Add to memory for replay
                agent.add_to_memory(current_state, next_states[best_action], reward, done)

                # Set current new state
                current_state = next_states[best_action]
                print(current_state)
                print(reward)

                steps += 1
            self.tetris_board.print_board(self.tetris.field_array)
            print("Total reward: " + str(total_reward))
            episodes.append(episode)
            rewards.append(total_reward)

            agent.replay()

            if agent.epsilon > agent.epsilon_min:
                agent.epsilon -= agent.epsilon_decay

    def play_game(self, game):
        self.train(game)
        pass


if __name__ == "__main__":
    tetris = Tetris()
    tetris_ai = TetrisAI(tetris)
    game = Game(tetris)
    tetris_ai.play_game(game)
