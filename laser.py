import pygame

LASER_SPEED = 2
PLAYER_START_Y = 655


class Laser:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path)
        self.x = 0
        self.y = PLAYER_START_Y
        self.state = "ready"

    def fire(self, player_x):
        self.x = player_x
        self.y = PLAYER_START_Y
        self.state = "fire"

    def update_position(self):
        if self.state == "fire":
            self.y -= LASER_SPEED
            if self.y <= 0:
                self.state = "ready"

    def draw(self, screen):
        if self.state == "fire":
            screen.blit(self.image, (self.x - 42, self.y - 26))
