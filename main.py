import pygame
from checkers.constants import SQUARE_SIZE, WIDTH, HEIGHT, FPS
from animations.animation import Animation

def main():

    animation = Animation()
    pygame.init()
    running = True
    clock = pygame.time.Clock()
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                animation.mouse_down(pos)

        animation.update()
    pygame.quit()


if __name__ == "__main__":
    main()
