import pygame
from checkers.constants import BLACK, TEXT_OFFSET

class Button:

    def __init__(self, x, y, width, height, color, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.message = text

    def clicked(self, position):
        x, y = position
        if self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height:
            return True
        return False

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.Font(None, 24)
        text = font.render(self.message, 1, BLACK)
        win.blit(text, (self.x + self.width // 5, (self.y * 2 + self.height) // 2 - TEXT_OFFSET))
