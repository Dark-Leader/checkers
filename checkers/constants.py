import pygame


ROWS = COLS = 8
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (135, 206, 250)
WIDTH = HEIGHT = 800
SQUARE_SIZE = WIDTH // ROWS
KING_IMAGE_OFFSET = 10
KING_SIZE = 20
crown = pygame.image.load("resources/crown.png")
crown = pygame.transform.scale(crown, (KING_SIZE, KING_SIZE))
POSSIBLE_MOVE_RADIUS = 15
