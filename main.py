import pygame
from checkers.game import Game
from checkers.constants import SQUARE_SIZE, WIDTH, HEIGHT

FPS = 60

def main():
    window = pygame.display.set_mode((WIDTH, HEIGHT + SQUARE_SIZE))
    pygame.display.set_caption("Checkers")
    game = Game(window)
    pygame.init()
    running = True
    clock = pygame.time.Clock()
    while running:
        clock.tick(FPS)
        if game.get_winner() is not None:
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                game.select(pos)

        game.update()
    pygame.quit()


if __name__ == "__main__":
    main()