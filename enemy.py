import pygame
import random

ENEMY_SPEED = 1
ENEMY_VERTICAL_MOVE = 40


class Enemy:
    def __init__(self, image_path, screen_width):
        self.image = pygame.image.load(image_path)
        self.x = random.randint(0, screen_width - 130)
        self.y = random.randint(10, 150)
        self.dx = ENEMY_SPEED

    def update_position(self, screen_width):
        self.x += self.dx
        if self.x <= 0 or self.x >= screen_width - 130:
            self.dx *= -1
            self.y += ENEMY_VERTICAL_MOVE

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
