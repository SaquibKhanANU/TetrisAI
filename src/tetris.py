from settings import *
from tetromino import Tetromino
import random


def get_new_tetromino():
    tetromino_type = random.choice(list(TETROMINOES.keys()))
    tetromino_info = TETROMINOES[tetromino_type]
    return Tetromino(tetromino_info['shape'], tetromino_info['color'])


class Tetris:
    def __init__(self):
        self.board_width = WIDTH
        self.board_height = HEIGHT
        self.grid_size = TILE_SIZE
        self.current_tetromino = get_new_tetromino()
        self.field_array = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.sprite_group = pg.sprite.Group()
        self.sprite_group.add(self.current_tetromino.sprite_group)

    def add_tetromino_to_array(self):
        for block in self.current_tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            self.field_array[y][x] = block

    def check_tetromino_landing(self):
        if self.current_tetromino.landing:
            self.add_tetromino_to_array()
            self.current_tetromino = get_new_tetromino()
            self.sprite_group.add(self.current_tetromino.sprite_group)

    # def control(self, key_pressed):
    #     if key_pressed == pg.K_LEFT:
    #         self.current_tetromino.move('left')
    #     elif key_pressed == pg.K_RIGHT:
    #         self.current_tetromino.move('right')
    def control(self, key_pressed):
        direction = None
        if key_pressed == pg.K_LEFT:
            direction = 'left'
        elif key_pressed == pg.K_RIGHT:
            direction = 'right'
        elif key_pressed == pg.K_DOWN:
            direction = 'down'
        move_direction = MOVE_DIRECTIONS.get(direction)

        if move_direction is not None:
            new_block_positions = [block.pos + move_direction for block in self.current_tetromino.blocks]
            is_collide = self.is_collide(new_block_positions)
            if not is_collide:
                self.current_tetromino.move(direction)
            elif direction == 'down':
                self.current_tetromino.landing = True

    def is_collide(self, positions):
        return not all(
            (0 <= int(position.x) < WIDTH and int(position.y) < HEIGHT) and (
                    int(position.y) < 0 or not self.field_array[int(position.y)][int(position.x)])
            for position in positions
        )

    def update(self, anim_trigger):
        if anim_trigger:
            self.control(pg.K_DOWN)
            self.check_tetromino_landing()
        self.sprite_group.update()

    def draw_grid(self, screen):
        for x in range(self.board_width):
            for y in range(self.board_height):
                pg.draw.rect(screen, (0, 0, 0), (x * self.grid_size, y * self.grid_size, TILE_SIZE, TILE_SIZE), 1)

    def draw(self, screen):
        self.draw_grid(screen)
        self.sprite_group.draw(screen)
