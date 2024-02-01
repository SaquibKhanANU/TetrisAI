from tetris import Tetris, TetrisBoard
import copy
from settings import *
from main import Game


class TetrisAI:
    def __init__(self, tetris):
        self.tetris = tetris
        self.tetris_board = TetrisBoard()

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
            for x in range(valid_xs):
                positions = [vec(x, 0) + block.pos - INIT_POS_OFFSET for block in piece.blocks]
                if not self.tetris_board.is_collide(positions, tetris_board_array_copy):
                    self.tetris_board.place_tetromino(piece, positions)
                    while not piece.landing:
                        self.tetris_board.move_block_down(piece, tetris_board_array_copy)
                    self.tetris_board.add_tetromino_to_board(piece, tetris_board_array_copy)
                    states[(x, i)] = self.tetris_board.get_board_properties(tetris_board_array_copy)
                    self.tetris_board.print_board(tetris_board_array_copy)

                    piece = copy.deepcopy(curr_piece)
                    tetris_board_array_copy = copy.deepcopy(tetris_board_array)
            self.tetris_board.rotate_block(curr_piece, tetris_board_array)
        print(curr_piece.rotation)
        print(self.tetris.current_tetromino.rotation)
        return states

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

    def play_game(self, gameRunner):
        counter = 1
        while True:
            if self.tetris.ai_move:
                x_pos, num_rotations = (counter, 0)
                self.ai_rotate(num_rotations)
                self.ai_move(x_pos)
                counter += 1
            gameRunner.check_events()
            gameRunner.update()
            gameRunner.draw()


def post_key_press_event(key):
    keydown_event = pg.event.Event(pg.KEYDOWN, {'key': key})
    pg.event.post(keydown_event)




if __name__ == "__main__":
    tetris = Tetris()
    tetris_ai = TetrisAI(tetris)
    game = Game(tetris)
    tetris_ai.play_game(game)
