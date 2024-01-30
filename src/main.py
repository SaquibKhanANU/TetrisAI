from tetris import Tetris
from settings import *
import sys


class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Tetris")
        self.screen = pg.display.set_mode((WIN_RES))
        self.clock = pg.time.Clock()
        self.set_timer()
        self.tetris = Tetris()

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

    def draw(self):
        self.screen.fill(color=LIGHT_BLACK)
        self.tetris.draw(self.screen)
        pg.display.flip()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == "__main__":
    game = Game()
    game.run()
