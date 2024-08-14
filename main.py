import pygame
from game_mechanics import GameMechanics

pygame.init()

if __name__ == '__main__':

    game = GameMechanics()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            else:
                game.handle_event(event)

        game.update()
        pygame.display.update()

    quit()