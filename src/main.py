from tetris import Tetris
from settings import *
import sys
import pygame.freetype as ft


class Game:
    def __init__(self, tetris):
        pg.init()
        pg.display.set_caption("Tetris")
        self.screen = pg.display.set_mode((WIN_RES))
        self.clock = pg.time.Clock()
        self.set_timer()
        self.tetris = tetris

    def set_timer(self):
        self.user_event = pg.USEREVENT + 0
        self.fast_user_event = pg.USEREVENT + 1
        self.anim_trigger = False
        self.fast_anim_trigger = False
        pg.time.set_timer(self.user_event, ANIM_TIME_INTERVAL)
        pg.time.set_timer(self.fast_user_event, FAST_ANIM_TIME_INTERVAL)

    def check_events(self):
        self.anim_trigger = False
        self.fast_anim_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN or event.type == pg.KEYUP:
                self.tetris.control(event)
            elif event.type == self.user_event:
                self.anim_trigger = True
            elif event.type == self.fast_user_event:
                self.fast_anim_trigger = True

    def update(self):
        self.tetris.update(self.anim_trigger, self.fast_anim_trigger)
        self.clock.tick(FPS)

    def draw_score(self):
        font = ft.Font(None, 8)

        font.render_to(self.screen, (WIN_W * 0.65, WIN_H * 0.2),
                       text=f'HEIGHT: {self.tetris.height}', fgcolor='WHITE',
                       size=TILE_SIZE * 0.5)
        font.render_to(self.screen, (WIN_W * 0.65, WIN_H * 0.3),
                       text=f'BUMPINESS: {self.tetris.bumpiness}', fgcolor='WHITE',
                       size=TILE_SIZE * 0.5)
        font.render_to(self.screen, (WIN_W * 0.65, WIN_H * 0.4),
                       text=f'NUM HOLES: {self.tetris.num_holes}', fgcolor='WHITE',
                       size=TILE_SIZE * 0.5)
        font.render_to(self.screen, (WIN_W * 0.65, WIN_H * 0.5),
                       text=f'SCORE: {self.tetris.score}', fgcolor='white',
                       size=TILE_SIZE * 0.5)
        font.render_to(self.screen, (WIN_W * 0.65, WIN_H * 0.6),
                       text=f'NUM_LINES: {self.tetris.num_lines}', fgcolor='WHITE',
                       size=TILE_SIZE * 0.5)
        font.render_to(self.screen, (WIN_W * 0.6, WIN_H * 0.7),
                       text=f'TOTAL_NUM_LINES: {self.tetris.total_num_lines}', fgcolor='WHITE',
                       size=TILE_SIZE * 0.5)
        font.render_to(self.screen, (WIN_W * 0.6, WIN_H * 0.8),
                       text=f'NUM_TETROMINOES: {self.tetris.num_tetrominoes}', fgcolor='WHITE',
                       size=TILE_SIZE * 0.5)

    def draw(self):
        self.screen.fill(color=LIGHT_BLACK)
        self.tetris.draw(self.screen)
        self.draw_score()
        pg.display.flip()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == "__main__":
    tetris = Tetris()
    game = Game(tetris)
    game.run()
