from .constants import SQUARE_SIZE, crown
import pygame


class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.is_king = False
        self.radius = 25

    def selected(self, row, col):
        return self.row == row and self.col == col

    def move(self, row, col):
        self.row = row
        self.col = col

    def draw(self, win):
        x_pos = int(SQUARE_SIZE * self.col + SQUARE_SIZE // 2)
        y_pos = int(SQUARE_SIZE * self.row + SQUARE_SIZE // 2)
        pygame.draw.circle(win, self.color, (x_pos, y_pos), self.radius)
        if self.is_king:
            win.blit(crown, (x_pos - crown.get_width() // 2, y_pos - crown.get_height() // 2))

    def make_king(self):
        self.is_king = True

    def get_color(self):
        return self.color

    def get_is_king(self):
        return self.is_king

    def get_row(self):
        return self.row

    def get_col(self):
        return self.col

    def set_row(self, new_row):
        self.row = new_row

    def set_col(self, new_col):
        self.col = new_col
