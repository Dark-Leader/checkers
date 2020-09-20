from .constants import ROWS, COLS, RED, BLACK, BLUE, WHITE, SQUARE_SIZE
from .piece import Piece
import pygame


class Board:

    def __init__(self):
        self.board = [[None] * ROWS for _ in range(COLS)]
        self.white_left = self.blue_left = 12
        self.blue_kings = self.white_kings = 0
        self.initialize_board()

    def initialize_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                if row % 2 == 0 and col % 2 == 1 and row < (ROWS // 2) - 1:
                    self.board[row][col] = Piece(row, col, BLUE)
                elif row % 2 == 1 and col % 2 == 0 and row < (ROWS // 2) - 1:
                    self.board[row][col] = Piece(row, col, BLUE)
                elif row % 2 == 1 and col % 2 == 0 and row >= (ROWS // 2) + 1:
                    self.board[row][col] = Piece(row, col, WHITE)
                elif row % 2 == 0 and col % 2 == 1 and row >= (ROWS // 2) + 1:
                    self.board[row][col] = Piece(row, col, WHITE)
                else:
                    continue

    def draw(self, win):
        self.draw_background(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.get_piece(row, col)
                if piece:
                    piece.draw(win)

    def draw_background(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, RED, (SQUARE_SIZE * col, SQUARE_SIZE * row, SQUARE_SIZE, SQUARE_SIZE))

    def get_piece(self, row, col):
        return self.board[row][col]

    def move(self, piece, row, col):
        start_row = piece.get_row()
        start_col = piece.get_col()
        self.board[row][col], self.board[start_row][start_col] = self.board[start_row][start_col], self.board[row][col]
        piece.move(row, col)
        if row == ROWS - 1 or row == 0:
            piece.make_king()

    def check_for_winner(self):
        if self.blue_left == 0:
            return WHITE
        elif self.white_left == 0:
            return BLUE
        else:
            return None

    def remove(self, pos):
        row, col = pos
        piece = self.get_piece(row, col)
        self.board[row][col] = None
        if piece is not None:
            if piece.get_color() == BLUE:
                self.white_left -= 1
            else:
                self.blue_left -= 1

    def find_legal_moves(self, piece, skipped=False):
        if piece.get_is_king():
            return self.find_legal_king_moves(piece, skipped)
        row = piece.get_row()
        col = piece.get_col()
        color = piece.get_color()
        left = col - 1
        right = col + 1
        top = row - 1
        bottom = row + 1
        legal_moves = {}
        if not skipped:
            if color == WHITE:
                if top >= 0:
                    if left >= 0:
                        top_left = self.get_piece(top, left)
                        if top_left is None:
                            legal_moves[(top, left)] = []
                        else:
                            if top_left.get_color() != color:
                                if left == 0 or top == 0:
                                    pass
                                else:
                                    possible_square = self.get_piece(top - 1, left - 1)
                                    if possible_square is None:
                                        legal_moves[(top - 1, left - 1)] = (top, left)
                    if right <= COLS - 1:
                        top_right = self.get_piece(top, right)
                        if top_right is None:
                            legal_moves[(top, right)] = None
                        else:
                            if top_right.get_color() != color:
                                if right == COLS - 1 or top == 0:
                                    pass
                                else:
                                    possible_square = self.get_piece(top - 1, right + 1)
                                    if possible_square is None:
                                        legal_moves[(top - 1, right + 1)] = (top, right)
            else:
                if bottom <= ROWS - 1:
                    if left >= 0:
                        bottom_left = self.get_piece(bottom, left)
                        if bottom_left is None:
                            legal_moves[(bottom, left)] = []
                        else:
                            if bottom_left.get_color() != color:
                                if left == 0 or bottom == ROWS - 1:
                                    pass
                                else:
                                    possible_square = self.get_piece(bottom + 1, left - 1)
                                    if possible_square is None:
                                        legal_moves[(bottom + 1, left - 1)] = (bottom, left)
                    if right <= COLS - 1:
                        bottom_right = self.get_piece(bottom, right)
                        if bottom_right is None:
                            legal_moves[(bottom, right)] = []
                        else:
                            if bottom_right.get_color() != color:
                                if right == COLS - 1 or bottom == ROWS - 1:
                                    pass
                                else:
                                    possible_square = self.get_piece(bottom + 1, right + 1)
                                    if possible_square is None:
                                        legal_moves[(bottom + 1, right + 1)] = (bottom, right)
        else:
            if color == WHITE:
                if top >= 1:
                    if left >= 1:
                        top_left = self.get_piece(top, left)
                        if top_left is not None and top_left.get_color() != color:
                            possible_square = self.get_piece(top - 1, left - 1)
                            if possible_square is None:
                                legal_moves[(top - 1, left - 1)] = (top, left)
                    if right <= COLS - 2:
                        top_right = self.get_piece(top, right)
                        if top_right is not None and top_right.get_color() != color:
                            possible_square = self.get_piece(top - 1, right + 1)
                            if possible_square is None:
                                legal_moves[(top - 1, right + 1)] = (top, right)
            else:
                if bottom <= ROWS - 2:
                    if left >= 1:
                        bottom_left = self.get_piece(bottom, left)
                        if bottom_left is not None and bottom_left.get_color() != color:
                            possible_square = self.get_piece(bottom + 1, left - 1)
                            if possible_square is None:
                                legal_moves[(bottom + 1, left - 1)] = (bottom, left)
                    if right <= COLS - 2:
                        bottom_right = self.get_piece(bottom + 1, right + 1)
                        if bottom_right is not None and bottom_right.get_color() != color:
                            possible_square = self.get_piece(bottom + 1, right + 1)
                            if possible_square is None:
                                legal_moves[(bottom + 1, right + 1)] = (bottom, right)
        return legal_moves

    def find_legal_king_moves(self, piece, skipped=False):
        row = piece.get_row()
        col = piece.get_col()
        color = piece.get_color()
        blocked = False
        left = col - 1
        right = col + 1
        bottom = row + 1
        top = row - 1
        legal_moves = {}
        if not skipped:
            while left >= 0 and bottom <= ROWS - 1:
                bottom_left = self.get_piece(bottom, left)
                if bottom_left is not None and bottom_left.get_color() == color:
                    break
                elif bottom_left is not None and bottom_left.get_color() != color and not blocked:
                    blocked = True
                elif bottom_left is not None and bottom_left.get_color() != color and blocked:
                    break
                elif bottom_left is None and not blocked:
                    legal_moves[(bottom, left)] = []
                elif bottom_left is None and blocked:
                    legal_moves[(bottom, left)] = (bottom - 1, left + 1)
                    break
                left -= 1
                bottom += 1
            blocked = False
            while right <= COLS - 1 and top >= 0:
                top_right = self.get_piece(top, right)
                if top_right is not None and top_right.get_color() == color:
                    break
                elif top_right is not None and top_right.get_color != color and not blocked:
                    blocked = True
                elif top_right is not None and top_right.get_color() != color and blocked:
                    break
                elif top_right is None and not blocked:
                    legal_moves[(top, right)] = []
                elif top_right is None and blocked:
                    legal_moves[(top, right)] = (top + 1, right - 1)
                    break
                elif top_right.get_color() != color:
                    blocked = True
                right += 1
                top -= 1
            blocked = False
            top = row - 1
            left = col - 1
            while left >= 0 and top >= 0:
                top_left = self.get_piece(top, left)
                if top_left is not None and top_left.get_color() == color:
                    break
                elif top_left is not None and top_left.get_color() != color and not blocked:
                    blocked = True
                elif top_left is not None and top_left.get_color() != color and blocked:
                    break
                elif top_left is None and not blocked:
                    legal_moves[(top, left)] = []
                elif top_left is None and blocked:
                    legal_moves[(top, left)] = (top + 1, left + 1)
                    break
                left -= 1
                top -= 1
            blocked = False
            right = col + 1
            bottom = row + 1
            while right <= COLS - 1 and bottom <= ROWS - 1:
                bottom_right = self.get_piece(bottom, right)
                if bottom_right is not None and bottom_right.get_color() == color:
                    break
                elif bottom_right is not None and bottom_right.get_color() != color and not blocked:
                    blocked = True
                elif bottom_right is not None and bottom_right.get_color() != color and blocked:
                    break
                elif bottom_right is None and not blocked:
                    legal_moves[(bottom, right)] = []
                elif bottom_right is None and blocked:
                    legal_moves[(bottom, right)] = (bottom - 1, right - 1)
                    break
                right += 1
                bottom += 1
        else:
            while top >= 0 and right <= COLS - 1:
                top_right = self.get_piece(top, right)
                if top_right is None and not blocked:
                    pass
                elif top_right is None and blocked:
                    legal_moves[(top, right)] = (top + 1, right - 1)
                elif top_right is not None and top_right.get_color() == color:
                    break
                elif top_right is not None and top_right.get_color() != color and not blocked:
                    blocked = True
                elif top_right is not None and top_right.get_color() != color and blocked:
                    break
                right += 1
                top -= 1
            top = row - 1
            blocked = False
            while top >= 0 and left >= 0:
                top_left = self.get_piece(top, left)
                if top_left is None and not blocked:
                    pass
                elif top_left is None and blocked:
                    legal_moves[top, left] = (top + 1, left + 1)
                elif top_left is not None and top_left.get_color() == color:
                    break
                elif top_left is not None and top_left.get_color() != color and not blocked:
                    blocked = True
                elif top_left is not None and top_left.get_color() != color and blocked:
                    break
                left -= 1
                top -= 1
            blocked = False
            right = col + 1
            left = col - 1
            while bottom <= ROWS - 1 and left >= 0:
                bottom_left = self.get_piece(bottom, left)
                if bottom_left is None and not blocked:
                    pass
                elif bottom_left is None and blocked:
                    legal_moves[bottom, left] = (bottom - 1, left + 1)
                elif bottom_left is not None and bottom_left.get_color() == color:
                    break
                elif bottom_left is not None and bottom_left.get_color() != color and not blocked:
                    blocked = True
                elif bottom_left is not None and bottom_left.get_color() != color and blocked:
                    break
                left -= 1
                bottom += 1
            bottom = row + 1
            blocked = False
            while bottom <= ROWS - 1 and right <= COLS - 1:
                bottom_right = self.get_piece(bottom, right)
                if bottom_right is None and not blocked:
                    pass
                elif bottom_right is None and blocked:
                    legal_moves[bottom, right] = (bottom - 1, right - 1)
                elif bottom_right is not None and bottom_right.get_color() == color:
                    break
                elif bottom_right is not None and bottom_right.get_color() != color and not blocked:
                    blocked = True
                elif bottom_right is not None and bottom_right.get_color() != color and blocked:
                    break
                right += 1
                bottom += 1
        return legal_moves
