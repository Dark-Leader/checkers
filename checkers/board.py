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

    def find_legal_moves(self, piece, skipped=False, mid_capture=False):
        if piece.get_is_king():
            return self.find_legal_king_move(piece, skipped, mid_capture)
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
                        bottom_right = self.get_piece(bottom, right)
                        if bottom_right is not None and bottom_right.get_color() != color:
                            possible_square = self.get_piece(bottom + 1, right + 1)
                            if possible_square is None:
                                legal_moves[(bottom + 1, right + 1)] = (bottom, right)
        return legal_moves

    def find_legal_pawn_moves(self, piece, skipped=False):
        row = piece.get_row()
        col = piece.get_col()
        color = piece.get_color()
        left = col - 1
        right = col + 1
        top = row - 1
        bottom = row + 1
        legal_moves = {}


        return legal_moves





    def find_legal_king_move(self, piece, skipped=False, mid_capture=False):
        legal_moves = {}
        piece_row = piece.get_row()
        piece_col = piece.get_col()
        top_left = False
        top_right = False
        bottom_left = False
        bottom_right = False
        if skipped:
            row, col = skipped
            if row > piece_row and col > piece_col:
                top_left = True
            elif row > piece_row and col < piece_col:
                top_right = True
            elif row < piece_row and col < piece_col:
                bottom_right = True
            else:
                bottom_left = True
        legal_moves.update(self.check_top_left_diagonal(piece, top_left, mid_capture))
        legal_moves.update(self.check_top_right_diagonal(piece, top_right, mid_capture))
        legal_moves.update(self.check_bottom_left_diagonal(piece, bottom_left, mid_capture))
        legal_moves.update(self.check_bottom_right_diagonal(piece, bottom_right, mid_capture))
        return legal_moves

    def check_top_left_diagonal(self, piece, skipped=False, mid_capture=False):
        color = piece.get_color()
        moves = {}
        row = piece.get_row()
        col = piece.get_col()
        left = col - 1
        top = row - 1
        blocked = False
        while top >= 0 and left >= 0:
            new_piece = self.get_piece(top, left)
            if not blocked and new_piece is None:
                if skipped or not mid_capture:
                    moves[(top, left)] = []
                else:
                    pass
            elif new_piece is None and blocked:
                moves[(top, left)] = blocked
            elif new_piece is not None and new_piece.get_color() == color:
                break
            elif new_piece is not None and new_piece.get_color() != color and not blocked:
                blocked = (top, left)
            elif new_piece is not None and new_piece.get_color() != color and blocked:
                break
            top -= 1
            left -= 1
        return moves

    def check_top_right_diagonal(self, piece, skipped=False, mid_capture=False):
        color = piece.get_color()
        moves = {}
        row = piece.get_row()
        col = piece.get_col()
        right = col + 1
        top = row - 1
        blocked = False
        while top >= 0 and right <= COLS - 1:
            new_piece = self.get_piece(top, right)
            if not blocked and new_piece is None:
                if skipped or not mid_capture:
                    moves[(top, right)] = []
                else:
                    pass
            elif new_piece is None and blocked:
                moves[(top, right)] = blocked
            elif new_piece is not None and new_piece.get_color() == color:
                break
            elif new_piece is not None and new_piece.get_color() != color and not blocked:
                blocked = (top, right)
            elif new_piece is not None and new_piece.get_color() != color and blocked:
                break
            top -= 1
            right += 1
        return moves

    def check_bottom_right_diagonal(self, piece, skipped=False, mid_capture=False):
        color = piece.get_color()
        moves = {}
        row = piece.get_row()
        col = piece.get_col()
        right = col + 1
        bottom = row + 1
        blocked = False
        while bottom <= ROWS - 1 and right <= COLS - 1:
            new_piece = self.get_piece(bottom, right)
            if not blocked and new_piece is None:
                if skipped or not mid_capture:
                    moves[(bottom, right)] = []
                else:
                    pass
            elif new_piece is None and blocked:
                moves[(bottom, right)] = blocked
            elif new_piece is not None and new_piece.get_color() == color:
                break
            elif new_piece is not None and new_piece.get_color() != color and not blocked:
                blocked = (bottom, right)
            elif new_piece is not None and new_piece.get_color() != color and blocked:
                break
            bottom += 1
            right += 1
        return moves

    def check_bottom_left_diagonal(self, piece, skipped=False, mid_capture=False):
        color = piece.get_color()
        moves = {}
        row = piece.get_row()
        col = piece.get_col()
        left = col - 1
        bottom = row + 1
        blocked = False
        while bottom <= ROWS - 1 and left >= 0:
            new_piece = self.get_piece(bottom, left)
            if not blocked and new_piece is None:
                if skipped or not mid_capture:
                    moves[(bottom, left)] = []
                elif False:
                    moves[(bottom, left)] = []
                else:
                    pass
            elif new_piece is None and blocked:
                moves[(bottom, left)] = blocked
            elif new_piece is not None and new_piece.get_color() == color:
                break
            elif new_piece is not None and new_piece.get_color() != color and not blocked:
                blocked = (bottom, left)
            elif new_piece is not None and new_piece.get_color() != color and blocked:
                break
            bottom += 1
            left -= 1
        return moves

