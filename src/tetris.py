from settings import *
from tetromino import Tetromino
import random
import time


class Tetris:
    def __init__(self):
        self.board_width = WIDTH
        self.board_height = HEIGHT
        self.grid_size = TILE_SIZE
        self.current_tetromino = None
        self.get_new_tetromino()
        self.field_array = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.sprite_group = pg.sprite.Group()
        self.sprite_group.add(self.current_tetromino.sprite_group)
        self.speed_up = False

    def add_tetromino_to_array(self):
        for block in self.current_tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            self.field_array[y][x] = block

    def get_new_tetromino(self):
        # tetromino_type = random.choice(list(TETROMINOES.keys()))
        tetromino_type = 'O'
        tetromino_info = TETROMINOES[tetromino_type]
        self.current_tetromino = Tetromino(tetromino_info['shape'], tetromino_info['color'])

    def check_tetromino_landing(self):
        if self.current_tetromino.landing:
            self.speed_up = False
            self.add_tetromino_to_array()
            self.get_new_tetromino()
            self.sprite_group.add(self.current_tetromino.sprite_group)

    def check_full_lines(self):
        row = HEIGHT - 1
        for y in range(HEIGHT - 1, -1, -1):
            for x in range(WIDTH):
                self.field_array[row][x] = self.field_array[y][x]
                if self.field_array[y][x]:
                    self.field_array[row][x].pos = vec(x, y)
            if sum(map(bool, self.field_array[y])) < WIDTH:
                row -= 1
            else:
                for x in range(WIDTH):
                    self.field_array[row][x].alive = False
                    self.field_array[row][x] = 0

    # def control(self, key_pressed):
    #     key_direction_mapping = {
    #         pg.K_LEFT: 'left',
    #         pg.K_RIGHT: 'right',
    #         pg.K_UP: 'rotate',
    #         pg.K_DOWN: 'down'
    #     }
    #     direction = key_direction_mapping.get(key_pressed)
    #     if direction is not None:
    #         if direction == 'rotate':
    #             pivot_pos = self.current_tetromino.blocks[0].pos
    #             positions = [block.rotate(pivot_pos) for block in self.current_tetromino.blocks]
    #             if not self.is_collide(positions):
    #                 self.current_tetromino.rotate(positions)
    #         elif direction == 'down':
    #             self.speed_up = True
    #         else:
    #             move_direction = MOVE_DIRECTIONS.get(direction)
    #             positions = [block.pos + move_direction for block in self.current_tetromino.blocks]
    #             if not self.is_collide(positions):
    #                 self.current_tetromino.move(direction)

    def control(self, event):
        key_direction_mapping = {
            pg.K_LEFT: 'left',
            pg.K_RIGHT: 'right',
            pg.K_UP: 'rotate',
            pg.K_DOWN: 'down',
            pg.K_SPACE: 'space'
        }

        if event.type == pg.KEYDOWN:
            key_code = event.key  # Access the key code directly
            direction = key_direction_mapping.get(key_code)
            if direction is not None:
                if direction == 'rotate':
                    pivot_pos = self.current_tetromino.blocks[0].pos
                    positions = [block.rotate(pivot_pos) for block in self.current_tetromino.blocks]
                    if not self.is_collide(positions):
                        self.current_tetromino.rotate(positions)
                elif direction == 'down' or direction == 'space':
                    self.speed_up = True
                else:
                    move_direction = MOVE_DIRECTIONS.get(direction)
                    positions = [block.pos + move_direction for block in self.current_tetromino.blocks]
                    if not self.is_collide(positions):
                        self.current_tetromino.move(direction)

        elif event.type == pg.KEYUP:
            key_code = event.key
            direction = key_direction_mapping.get(key_code)
            if direction == 'down':
                self.speed_up = False

    def is_collide(self, positions):
        return not all(
            (0 <= int(position.x) < WIDTH and int(position.y) < HEIGHT) and (
                    int(position.y) < 0 or not self.field_array[int(position.y)][int(position.x)])
            for position in positions
        )

    def update(self, anim_trigger, fast_anim_trigger):
        trigger = [anim_trigger, fast_anim_trigger][self.speed_up]
        if trigger:
            move_direction = MOVE_DIRECTIONS.get('down')
            positions = [block.pos + move_direction for block in self.current_tetromino.blocks]
            if not self.is_collide(positions):
                self.current_tetromino.update()
            else:
                self.current_tetromino.landing = True
        self.check_tetromino_landing()
        self.check_full_lines()
        self.sprite_group.update()

    def draw_grid(self, screen):
        for x in range(self.board_width):
            for y in range(self.board_height):
                pg.draw.rect(screen, BLACK, (x * self.grid_size, y * self.grid_size, TILE_SIZE, TILE_SIZE), 1)

    def draw(self, screen):
        self.draw_grid(screen)
        self.sprite_group.draw(screen)
