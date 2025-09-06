import random
from collections import deque
from lib import visuals
from lib.constants import pieces

class TetrisGame:
    def __init__(self):
        self.board = [[0] * 10 for _ in range(20)]
        self.queue = deque()
        self.score = 0

    def set_board(self, newBoard):
        self.board = newBoard

    def refill_bag(self):
        bag = list("jlsziot")
        random.shuffle(bag)
        self.queue.extend(bag)

    def next_piece(self):
        if not self.queue:
            self.refill_bag()
        return self.queue.popleft()

    def clear_lines(self):
        self.board = [row for row in self.board if any(c == 0 for c in row)]
        cleared = 20 - len(self.board)
        self.board = [[0] * 10 for _ in range(cleared)] + self.board
        self.score += [0, 1, 2, 4][cleared-1]

    def is_valid_position(self, piece, row, col):
        for r_offset, r in enumerate(piece):
            for c_offset, tile in enumerate(r):
                if tile != 0:
                    board_r, board_c = row + r_offset, col + c_offset
                    if not (0 <= board_r < 20 and 0 <= board_c < 10):
                        return False
                    if self.board[board_r][board_c] != 0:
                        return False
        return True

    def place_piece(self, piece, row, col):
        for r_offset, r in enumerate(piece):
            for c_offset, tile in enumerate(r):
                if tile != 0:
                    self.board[row + r_offset][col + c_offset] = tile

    def drop(self, piece, pos):
        final_row = 0
        for r in range(20):
            if self.is_valid_position(piece, r, pos):
                final_row = r
            else:
                break
        self.place_piece(piece, final_row, pos)

    def isGameOver(self):
        return self.board[0] != [0] * 10

    def draw(self):
        visuals.draw(self.board)

