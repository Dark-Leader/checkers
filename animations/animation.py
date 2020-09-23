import pygame
from checkers.game import Game
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE
from .end_screen import EndScreen


class Animation:

    def __init__(self):
        self.win = pygame.display.set_mode((WIDTH, HEIGHT + SQUARE_SIZE))
        pygame.display.set_caption("Checkers")
        self.game = Game(self.win)
        self.game_over = False
        self.end_screen = EndScreen(self.win, None)

    def update(self):
        result = self.game.get_winner()
        if self.game_over:
            self.game.board.draw(self.win)
            self.end_screen.draw()
        if result:
            self.end_screen.set_winner(result)
            self.game_over = True
        else:
            self.game.update()
        pygame.display.flip()

    def mouse_down(self, position):
        if not self.game_over:
            self.game.select(position)
        else:
            if self.end_screen.clicked(position):
                self.game.reset()
                self.game_over = False
