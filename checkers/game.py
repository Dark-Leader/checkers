from .board import Board
from .constants import WHITE, BLUE, LIGHT_BLUE, SQUARE_SIZE, POSSIBLE_MOVE_RADIUS, WIDTH, HEIGHT, ROWS, BROWN
import pygame
from .shapes.button import Button


class Game:
    def __init__(self, win):
        self.win = win
        self._initialize()

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        self.draw_turn()
        if self.mid_capture:
            self.button.draw(self.win)
        pygame.display.flip()

    def _initialize(self):
        self.board = Board()
        self.selected = None
        self.turn = WHITE
        self.valid_moves = {}
        self.button = Button(WIDTH // 2 + SQUARE_SIZE * 2, HEIGHT + SQUARE_SIZE // 3, SQUARE_SIZE, SQUARE_SIZE // 3,
                             BROWN, "End Turn")
        self.mid_capture = False

    def draw_turn(self):
        pygame.draw.rect(self.win, LIGHT_BLUE, (0, HEIGHT, WIDTH, SQUARE_SIZE))
        message = "White's turn" if self.turn == WHITE else "Blue's turn"
        font = pygame.font.Font(None, 30)
        text = font.render(message, 1, self.turn)
        self.win.blit(text, (WIDTH // 2 - SQUARE_SIZE // 2, HEIGHT + SQUARE_SIZE // 2.5))

    def get_winner(self):
        return self.board.check_for_winner(self.turn)

    def select(self, position):
        row, col = self.get_position(position)
        if row <= ROWS - 1:
            if self.selected:
                result = self._move(row, col)
                if not result:
                    self.selected = None
                    self.select(position)
            piece = self.board.get_piece(row, col)
            if piece is not None and piece.get_color() == self.turn:
                self.selected = piece
                if not self.mid_capture:
                    self.valid_moves = self.board.find_legal_moves(piece)
                return True
            return False
        else:
            if self.button.clicked(position) and self.mid_capture:
                self.change_turn()

    @staticmethod
    def get_position(position):
        x, y = position
        row = int(y // SQUARE_SIZE)
        col = int(x // SQUARE_SIZE)
        return row, col

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and (piece is None) and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
                self.valid_moves = self.board.find_legal_moves(self.board.get_piece(row, col), skipped, True)
                if not bool(self.valid_moves):
                    self.change_turn()
                else:
                    self.mid_capture = True
            else:
                self.change_turn()
        else:
            return False
        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, LIGHT_BLUE, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2),
                                                      int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), POSSIBLE_MOVE_RADIUS)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == WHITE:
            self.turn = BLUE
        else:
            self.turn = WHITE
        self.mid_capture = False

    def reset(self):
        self._initialize()
