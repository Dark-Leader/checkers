import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, LIGHT_BLUE, BLACK, WHITE, BLUE, TEXT_OFFSET
from checkers.shapes.button import Button


class EndScreen:

    def __init__(self, window, winner):
        self.win = window
        self.reset_button = Button(WIDTH // 2 - SQUARE_SIZE * 1.5, HEIGHT,
                                   SQUARE_SIZE * 3, SQUARE_SIZE, LIGHT_BLUE)
        self.winner = winner

    def draw(self):
        message = "Game Over!"
        if self.winner == WHITE:
            message += " White Won"
        elif self.winner == BLUE:
            message += " Blue Won"
        else:
            message += " It's a draw"
        font = pygame.font.Font(None, 24)
        game_over_message = font.render(message, 1, BLACK)
        self.reset_button.draw(self.win)
        self.win.blit(game_over_message, (WIDTH // 2 - SQUARE_SIZE, HEIGHT + SQUARE_SIZE // 2 - TEXT_OFFSET * 4))
        play_again_message = font.render("PLAY AGAIN", 1, BLACK)
        self.win.blit(play_again_message, (WIDTH // 2 - SQUARE_SIZE // 2, HEIGHT + SQUARE_SIZE // 2 + TEXT_OFFSET))


    def clicked(self, position):
        return self.reset_button.clicked(position)

    def set_winner(self, new_winner):
        self.winner = new_winner
            