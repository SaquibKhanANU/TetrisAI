from settings import *


class Block(pg.sprite.Sprite):
    def __init__(self, pos, color):
        self.pos = vec(pos) + INIT_POS_OFFSET

        super().__init__()
        self.image = pg.Surface([TILE_SIZE, TILE_SIZE])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos * TILE_SIZE

    def set_rect_pos(self):
        self.rect.topleft = self.pos * TILE_SIZE

    # def is_collide(self, pos):
    #     x, y = int(pos.x), int(pos.y)
    #     if 0 <= x < WIDTH and y < HEIGHT:
    #         return False
    #     return True

    def update(self):
        self.set_rect_pos()


class Tetromino:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.rotation = 0  # 0 0/360 # 1 90 # 2 180 # 3 270
        self.blocks = []
        self.sprite_group = pg.sprite.Group()
        self.landing = False
        self.create_blocks()

    # def update(self):
    #     self.move('down')

    # def move(self, direction):
    #     move_direction = MOVE_DIRECTIONS[direction]
    #     new_block_positions = [block.pos + move_direction for block in self.blocks]
    #     is_collide = self.is_collide(new_block_positions)
    #     if not is_collide:
    #         for block in self.blocks:
    #             block.pos += move_direction
    #     elif direction == 'down':
    #         self.landing = True

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

    # def is_collide(self, block_positions):
    #     return any(map(Block.is_collide, self.blocks, block_positions))
