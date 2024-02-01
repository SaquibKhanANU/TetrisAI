from settings import *
import copy


class Block(pg.sprite.Sprite):
    def __init__(self, pos, color):
        self.pos = vec(pos)
        self.alive = True
        self.color = color

        super().__init__()
        self.image = pg.Surface([TILE_SIZE, TILE_SIZE])
        pg.draw.rect(self.image, color, (1, 1, TILE_SIZE - 2, TILE_SIZE - 2), border_radius=2)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos * TILE_SIZE

    def is_alive(self):
        if not self.alive:
            self.kill()

    def rotate(self, pivot_pos):
        translate = self.pos - pivot_pos
        rotated = translate.rotate(90)
        return rotated + pivot_pos

    def set_rect_pos(self):
        self.rect.topleft = self.pos * TILE_SIZE

    def shift_block(self, shift):
        self.pos = self.pos + shift

    def update(self):
        self.is_alive()
        self.set_rect_pos()

    def __str__(self):
        return f"1"
        # return f'{self.pos}, {self.rect.topleft}'

    def __reduce__(self):
        # Customizing the pickling process by returning a tuple
        # containing the class, constructor arguments, and instance state.
        return self.__class__, (self.pos, self.color)



class Tetromino:
    def __init__(self, shape, color, type):
        self.type = type
        self.shape = shape
        self.color = color
        self.rotation = 0  # 0 0/360 # 1 90 # 2 180 # 3 270
        self.blocks = []
        self.sprite_group = pg.sprite.Group()
        self.landing = False
        self.create_blocks()

    def update(self):
        self.move('down')

    def move(self, direction):
        move_direction = MOVE_DIRECTIONS[direction]
        for block in self.blocks:
            block.pos += move_direction

    def create_blocks(self):
        self.sprite_group.empty()
        for pos in self.shape:
            block = Block((pos[0], pos[1]), self.color)
            self.blocks.append(block)
            self.sprite_group.add(block)

    def rotate(self, new_block_positions):
        self.rotation = (self.rotation + 1) % 4
        for i, block in enumerate(self.blocks):
            block.pos = new_block_positions[i]

    def shift_blocks(self, shift):
        for block in self.blocks:
            block.shift_block(shift)

    def get_width(self):
        blocks_x = [block.pos.x for block in self.blocks]
        max_x = max(blocks_x)
        min_x = min(blocks_x)
        return int(max_x - min_x + 1)

    def __str__(self):
        return f"{self.type}"
