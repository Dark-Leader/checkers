from .constants import ROWS, COLS, RED, BLACK, BLUE, WHITE, SQUARE_SIZE
from .piece import Piece
import pygame


class Board:

    def __init__(self):
        self.board = [[None] * ROWS for _ in range(COLS)]
        self.white_left = self.blue_left = 12
        self.winner = None
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
                    self.board[row][col] = None

    def draw(self, win):
        self.draw_background(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.get_piece(row, col)
                if piece:
                    piece.draw(win)

    @staticmethod
    def draw_background(win):
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
        if piece.get_color() == WHITE and row == 0 and not piece.get_is_king():
            piece.make_king()
        elif piece.get_color() == BLUE and row == ROWS - 1 and not piece.get_is_king():
            piece.make_king()

    def check_for_winner(self, color):
        if self.blue_left == 0:
            self.winner = WHITE
        elif self.white_left == 0:
            self.winner = BLUE
        elif self.check_stalemate(color):
            if self.white_left > self.blue_left:
                self.winner = WHITE
            elif self.white_left == self.blue_left:
                self.winner = "Draw"
            else:
                self.winner = BLUE
        if self.winner == WHITE:
            print("White Won!")
        elif self.winner == BLUE:
            print("Blue won!")
        elif self.winner == "Draw":
            print("It's a Draw!")
        return self.winner

    def check_stalemate(self, color):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.get_piece(row, col)
                if piece and piece.get_color() == color:
                    moves = self.find_legal_moves(piece)
                    if bool(moves):
                        return False
        return True

    def remove(self, pos):
        row, col = pos
        piece = self.get_piece(row, col)
        self.board[row][col] = None
        if piece is not None:
            if piece.get_color() == BLUE:
                self.blue_left -= 1
            else:
                self.white_left -= 1

    def find_legal_moves(self, piece, skipped=False, mid_capture=False):
        if piece.get_is_king():
            return self.find_legal_king_move(piece, skipped, mid_capture)
        color = piece.get_color()
        legal_moves = {}
        if color == WHITE:
            legal_moves.update(self.find_top_left_pawn_moves(piece, skipped))
            legal_moves.update(self.find_top_right_pawn_moves(piece, skipped))
        else:
            legal_moves.update(self.find_bottom_left_pawn_moves(piece, skipped))
            legal_moves.update(self.find_bottom_right_pawn_moves(piece, skipped))
        return legal_moves

    def find_top_left_pawn_moves(self, piece, skipped=False, count=2):
        moves = {}
        row, col, color = self.get_row_col_color(piece)
        top = row - 1
        left = col - 1
        blocked = False
        while top >= 0 and left >= 0 and count > 0:
            top_left = self.get_piece(top, left)
            if not blocked and top_left is None and not skipped:
                moves[(top, left)] = []
                break
            elif top_left is not None and top_left.get_color() == color:
                break
            elif top_left is not None and top_left.get_color() != color:
                blocked = (top, left)
            elif blocked and top_left is None:
                moves[(top, left)] = blocked
            top -= 1
            left -= 1
            count -= 1
        return moves

    def find_top_right_pawn_moves(self, piece, skipped=False, count=2):
        moves = {}
        row, col, color = self.get_row_col_color(piece)
        top = row - 1
        right = col + 1
        blocked = False
        while top >= 0 and right <= COLS - 1 and count > 0:
            top_right = self.get_piece(top, right)
            if not blocked and top_right is None and not skipped:
                moves[(top, right)] = []
                break
            elif top_right is not None and top_right.get_color() == color:
                break
            elif top_right is not None and top_right.get_color() != color:
                blocked = (top, right)
            elif blocked and top_right is None:
                moves[(top, right)] = blocked
            top -= 1
            right += 1
            count -= 1
        return moves

    def find_bottom_right_pawn_moves(self, piece, skipped=False, count=2):
        moves = {}
        row, col, color = self.get_row_col_color(piece)
        bottom = row + 1
        right = col + 1
        blocked = False
        while bottom <= ROWS - 1 and right <= COLS - 1 and count > 0:
            bottom_right = self.get_piece(bottom, right)
            if not blocked and bottom_right is None and not skipped:
                moves[(bottom, right)] = []
                break
            elif bottom_right is not None and bottom_right.get_color() == color:
                break
            elif bottom_right is not None and bottom_right.get_color() != color:
                blocked = (bottom, right)
            elif blocked and bottom_right is None:
                moves[(bottom, right)] = blocked
            bottom += 1
            right += 1
            count -= 1
        return moves

    def find_bottom_left_pawn_moves(self, piece, skipped=False, count=2):
        moves = {}
        row, col, color = self.get_row_col_color(piece)
        bottom = row + 1
        left = col - 1
        blocked = False
        while bottom <= ROWS - 1 and left >= 0 and count > 0:
            bottom_right = self.get_piece(bottom, left)
            if not blocked and bottom_right is None and not skipped:
                moves[(bottom, left)] = []
                break
            elif bottom_right is not None and bottom_right.get_color() == color:
                break
            elif bottom_right is not None and bottom_right.get_color() != color:
                blocked = (bottom, left)
            elif blocked and bottom_right is None:
                moves[(bottom, left)] = blocked
            bottom += 1
            left -= 1
            count -= 1
        return moves

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
        moves = {}
        row, col, color = self.get_row_col_color(piece)
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
        moves = {}
        row, col, color = self.get_row_col_color(piece)
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
        moves = {}
        row, col, color = self.get_row_col_color(piece)
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
        moves = {}
        row, col, color = self.get_row_col_color(piece)
        left = col - 1
        bottom = row + 1
        blocked = False
        while bottom <= ROWS - 1 and left >= 0:
            new_piece = self.get_piece(bottom, left)
            if not blocked and new_piece is None:
                if skipped or not mid_capture:
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

    @staticmethod
    def get_row_col_color(piece):
        return piece.get_row(), piece.get_col(), piece.get_color()
