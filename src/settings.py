import pygame as pg

# CONSTANTS
STARTING_ROW = 0
STARTING_COL = 4
TILE_SIZE = 40
HEIGHT = 20
WIDTH = 10

WIN_RES = WIN_WIDTH, WIN_HEIGHT = WIDTH * TILE_SIZE, HEIGHT * TILE_SIZE
FPS = 60
ANIM_TIME_INTERVAL = 150

vec = pg.math.Vector2
INIT_POS_OFFSET = vec((WIDTH // 2 - 1, 0)) // 2
MOVE_DIRECTIONS = {'left': vec(-1, 0), 'right': vec(1, 0), 'down': vec(0, 1)}

TETROMINOES = {
    'T': {
        'color': pg.Color('red'),
        'shape': [(0, 0), (-1, 0), (1, 0), (0, -1)],
    },
    'O': {
        'color': pg.Color('orange'),
        'shape': [(0, 0), (0, -1), (1, 0), (1, -1)],
    },
    'J': {
        'color': pg.Color('blue'),
        'shape': [(0, 0), (-1, 0), (0, -1), (0, -2)],
    },
    'L': {
        'color': pg.Color('purple'),
        'shape': [(0, 0), (1, 0), (0, -1), (0, -2)],
    },
    'I': {
        'color': pg.Color('pink'),
        'shape': [(0, 0), (0, 1), (0, -1), (0, -2)],
    },
    'S': {
        'color': pg.Color('yellow'),
        'shape': [(0, 0), (-1, 0), (0, -1), (1, -1)],
    },
    'Z': {
        'color': pg.Color('green'),
        'shape': [(0, 0), (1, 0), (0, -1), (-1, -1)],
    },
}