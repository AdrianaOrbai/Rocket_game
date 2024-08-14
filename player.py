import pygame

PLAYER_START_X = 650
PLAYER_START_Y = 655
PLAYER_SPEED = 0.5


class Player:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path)
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.dx = 0

    def move_left(self):
        self.dx = -PLAYER_SPEED

    def move_right(self):
        self.dx = PLAYER_SPEED

    def stop(self):
        self.dx = 0

    def update_position(self, screen_width):
        self.x += self.dx
        self.x = max(20, min(self.x, screen_width - 90))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

