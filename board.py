import math
import random

block_shapes = [
    # I Block
    [[1], [1], [1], [1]],
    # O Block
    [[1, 1],
     [1, 1]],
    # S Block
    [[0, 1, 1],
     [1, 1, 0]],
    # Z Block
    [[1, 1, 0],
     [0, 1, 1]],
    # J Block
    [[0, 1],
     [0, 1],
     [1, 1]],
    # L Block
    [[1, 0],
     [1, 0],
     [1, 1]],
    # T Block
    [[0, 1, 0],
     [1, 1, 1]],
]

ACTIONS = ['nop', 'rotate', 'down', 'left', 'right', 'drop']
ACTIONS_MAP = {k:v for k, v in enumerate(ACTIONS)}

class Board:
    def __init__(self, height = 20, width = 10, seed=None):
        self.height = height
        self.width = width
        
        if seed is not None:
            random.seed(seed)

        self.reset()

    def reset(self):
        self.board = self._create_new_board()

        self.game_over = False
        self.score = 0

        self._minos = []

        self._minos += self._gen_minos()
        self._minos += self._gen_minos()

        self.current_block = self._minos.pop(0)
        self.current_block_pos = None

        self._place_new_block()

    def is_game_over(self):
        return self.game_over

    def act(self, action_number):
        action = ACTIONS_MAP[action_number]
        if action == 'rotate':
            self._rotate_block()
        elif action == 'down':
            self._move_block('down')
        elif action == 'left':
            self._move_block('left')
        elif action == 'right':
            self._move_block('right')
        elif action == 'drop':
            self._drop()
        else:
            pass

    def get_next(self):
        return self._minos[:3]

    def add_penalty_minos(self, nlines):
        space = random.randrange(0, self.width)
        penalty = [[0 if i == space else 1 for i in range(self.width)] for _ in range(nlines)]
        self.board = (self.board + penalty)[nlines:]

    def _rotate_block(self):
        rotated_shape = list(map(list, zip(*self.current_block.shape[::-1])))

        if self._can_move(self.current_block_pos, rotated_shape):
            self.current_block.shape = rotated_shape

    def _move_block(self, direction):
        pos = self.current_block_pos
        if direction == "left":
            new_pos = [pos[0], pos[1] - 1]
        elif direction == "right":
            new_pos = [pos[0], pos[1] + 1]
        elif direction == "down":
            new_pos = [pos[0] + 1, pos[1]]
        else:
            raise ValueError("wrong directions")

        if self._can_move(new_pos, self.current_block.shape):
            self.current_block_pos = new_pos
        elif direction == "down":
            self._land_block()
            self._burn()
            self._place_new_block()

    def _drop(self):
        while self._can_move((self.current_block_pos[0] + 1, self.current_block_pos[1]), self.current_block.shape):
            self._move_block("down")

        self._land_block()
        self._burn()
        self._place_new_block()

    def _gen_minos(self):
        box = list(range(7))
        random.shuffle(box)

        return [Block(i) for i in box]

    def _create_new_board(self):
        return [[0 for _ in range(self.width)] for _ in range(self.height)]

    def _place_new_block(self):
        self.score += 5

        if len(self._minos) < 10:
            self._minos += self._gen_minos()
        
        self.current_block = self._minos.pop(0)

        size = Block.get_size(self.current_block.shape)
        col_pos = math.floor((self.width - size[1]) / 2)
        self.current_block_pos = [0, col_pos]

        if self._check_overlapping(self.current_block_pos, self.current_block.shape):
            self.game_over = True

    def _land_block(self):

        size = Block.get_size(self.current_block.shape)
        for row in range(size[0]):
            for col in range(size[1]):
                if self.current_block.shape[row][col] == 1:
                    self.board[self.current_block_pos[0] + row][self.current_block_pos[1] + col] = 1

    def _burn(self):
        for row in range(self.height):
            if all(col != 0 for col in self.board[row]):
                for r in range(row, 0, -1):
                    self.board[r] = self.board[r - 1]
                self.board[0] = [0 for _ in range(self.width)]
                self.score += 100

    def _check_overlapping(self, pos, shape):
        size = Block.get_size(shape)
        for row in range(size[0]):
            for col in range(size[1]):
                if shape[row][col] == 1:
                    if self.board[pos[0] + row][pos[1] + col] == 1:
                        return True
        return False

    def _can_move(self, pos, shape):
        size = Block.get_size(shape)
        if pos[1] < 0 or pos[1] + size[1] > self.width or pos[0] + size[0] > self.height:
            return False

        return not self._check_overlapping(pos, shape)

    @property
    def __dict__(self):
        return {
            'board': self.board,
            'next': list(map(lambda x: x.type, self.get_next())),
            'score': self.score,
            'block': self.current_block.type,
            'shape': self.current_block.shape,
            'pos': self.current_block_pos
        }

class Block:
    def __init__(self, block_type):
        self.shape = block_shapes[block_type]
        self.color = block_type + 1
        self.type = ['I', 'O', 'S', 'Z', 'J', 'L', 'T'][block_type]

    def flip(self):
        self.shape = list(map(list, self.shape[::-1]))

    def _get_rotated(self):
        return list(map(list, zip(*self.shape[::-1])))

    def size(self):
        return self.get_size(self.shape)

    @staticmethod
    def get_size(shape):
        return [len(shape), len(shape[0])]

    def __str__(self):
        return self.type

    def __repr__(self):
        return self.__str__()
