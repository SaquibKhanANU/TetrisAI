from settings import *
from src import tetromino
from tetromino import Tetromino
import random


class TetrisBoard:
    @staticmethod
    def is_game_over(tetromino):
        if tetromino.blocks[0].pos.y == INIT_POS_OFFSET[1]:
            pg.time.wait(100)
            return True

    @staticmethod
    def clear_lines(tetris_board):
        row = HEIGHT - 1
        for y in range(HEIGHT - 1, -1, -1):
            for x in range(WIDTH):
                tetris_board[row][x] = tetris_board[y][x]
                if tetris_board[y][x]:
                    tetris_board[row][x].pos = vec(x, y)
            if sum(map(bool, tetris_board[y])) < WIDTH:
                row -= 1
            else:
                for x in range(WIDTH):
                    tetris_board[row][x].alive = False
                    tetris_board[row][x] = 0

    @staticmethod
    def add_tetromino_to_board(tetromino, tetris_board):
        for block in tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            tetris_board[y][x] = block

    @staticmethod
    def is_collide(positions, tetris_board):
        return not all(
            (0 <= int(position.x) < WIDTH and int(position.y) < HEIGHT) and (
                    int(position.y) < 0 or not tetris_board[int(position.y)][int(position.x)])
            for position in positions
        )

    def move_block_down(self, tetromino, tetris_board):
        move_direction = MOVE_DIRECTIONS.get('down')
        positions = [block.pos + move_direction for block in tetromino.blocks]
        if not self.is_collide(positions, tetris_board):
            tetromino.update()
        else:
            tetromino.landing = True

    def rotate_block(self, tetromino, tetris_board):
        pivot_pos = tetromino.blocks[0].pos
        positions = [block.rotate(pivot_pos) for block in tetromino.blocks]
        if not self.is_collide(positions, tetris_board):
            tetromino.rotate(positions)

    @staticmethod
    def place_tetromino(tetromino, positions):
        for block, position in zip(tetromino.blocks, positions):
            block.pos = position
            block.set_rect_pos()

    @staticmethod
    def calculate_num_holes(tetris_board):
        holes_count = 0
        for col in range(len(tetris_board[0])):
            found_block = False
            for row in range(len(tetris_board)):
                if tetris_board[row][col] != 0:
                    found_block = True
                elif tetris_board[row][col] == 0 and found_block:
                    holes_count += 1
        return holes_count

    @staticmethod
    def calculate_height_and_bumpiness(tetris_board):
        column_heights = []
        max_height = 0
        for col in range(len(tetris_board[0])):
            for row in range(len(tetris_board)):
                if tetris_board[row][col] != 0:
                    # Found the top non-empty block in this column
                    height = len(tetris_board) - row
                    column_heights.append(height)
                    break  # Move to the next column

        bumpiness = sum(abs(column_heights[i] - column_heights[i + 1]) for i in range(len(column_heights) - 1))
        if column_heights:
            max_height = max(column_heights)
        return max_height, bumpiness

    @staticmethod
    def calculate_num_lines(tetris_board):
        rows_to_clear = [y for y in range(HEIGHT) if sum(map(bool, tetris_board[y])) == WIDTH]
        return rows_to_clear

    def get_board_properties(self, tetris_board):
        height, bumpiness = self.calculate_height_and_bumpiness(tetris_board)
        num_holes = self.calculate_num_holes(tetris_board)
        num_lines = len(self.calculate_num_lines(tetris_board))
        return num_lines, num_holes, height, bumpiness


    @staticmethod
    def print_board(tetris_board):
        print("BOARD:")
        for row in tetris_board:
            print(' '.join(map(str, row)))


class Tetris:
    def __init__(self):
        self.board_width = WIDTH
        self.board_height = HEIGHT
        self.grid_size = TILE_SIZE
        self.current_tetromino = None
        self.field_array = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.tetris_board = TetrisBoard()
        self.get_new_tetromino()

        self.sprite_group = pg.sprite.Group()
        self.sprite_group.add(self.current_tetromino.sprite_group)
        self.speed_up = False

        self.score = 0
        self.num_holes = 0
        self.num_lines = 0
        self.height = 0
        self.bumpiness = 0
        self.total_num_lines = 0
        self.num_tetrominoes = 0
        self.points_per_line = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}


        self.game_over = False
        self.ai_move = True

    def check_tetromino_landing(self):
        if self.current_tetromino.landing:
            if self.tetris_board.is_game_over(self.current_tetromino):
                self.game_over = True
            else:
                self.tetris_board.add_tetromino_to_board(self.current_tetromino, self.field_array)
                self.ai_move = True
                self.sprite_group.add(self.current_tetromino.sprite_group)
                self.num_lines, self.num_holes, self.height, self.bumpiness = (
                    self.tetris_board.get_board_properties(self.field_array))
                self.score += self.points_per_line[self.num_lines]
                self.total_num_lines += self.num_lines
                self.num_tetrominoes += 1
                self.get_new_tetromino()
                # self.tetris_board.print_board(self.field_array)

    def get_new_tetromino(self):
        tetromino_type = random.choice(list(TETROMINOES.keys()))
        tetromino_info = TETROMINOES[tetromino_type]
        self.current_tetromino = Tetromino(tetromino_info['shape'], tetromino_info['color'], tetromino_type)
        self.current_tetromino.shift_blocks(INIT_POS_OFFSET)

    def control(self, event):
        key_direction_mapping = {
            pg.K_LEFT: 'left',
            pg.K_RIGHT: 'right',
            pg.K_UP: 'rotate',
            pg.K_DOWN: 'down',
            pg.K_SPACE: 'space'
        }

        if event.type == pg.KEYDOWN:
            key_code = event.key
            direction = key_direction_mapping.get(key_code)
            if direction is not None:
                if direction == 'rotate':
                    self.tetris_board.rotate_block(self.current_tetromino, self.field_array)
                elif direction == 'down' or direction == 'space':
                    self.speed_up = True
                else:
                    move_direction = MOVE_DIRECTIONS.get(direction)
                    positions = [block.pos + move_direction for block in self.current_tetromino.blocks]
                    if not self.tetris_board.is_collide(positions, self.field_array):
                        self.current_tetromino.move(direction)

        elif event.type == pg.KEYUP:
            key_code = event.key
            direction = key_direction_mapping.get(key_code)
            if direction == 'down':
                self.speed_up = False

    def update(self, anim_trigger, fast_anim_trigger):
        self.ai_move = False
        trigger = [anim_trigger, fast_anim_trigger][self.speed_up]
        if not self.game_over:
            if trigger:
                self.tetris_board.move_block_down(self.current_tetromino, self.field_array)
            if self.current_tetromino.landing:
                self.speed_up = False
            self.check_tetromino_landing()
            self.tetris_board.clear_lines(self.field_array)
            self.sprite_group.update()

    def draw_grid(self, screen):
        for x in range(self.board_width):
            for y in range(self.board_height):
                pg.draw.rect(screen, BLACK, (x * self.grid_size, y * self.grid_size, TILE_SIZE, TILE_SIZE), 1)

    def draw(self, screen):
        self.draw_grid(screen)
        self.sprite_group.draw(screen)

    def reset(self):
        self.__init__()
