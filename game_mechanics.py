import pygame
import math
import random
import json
from player import Player, PLAYER_START_Y, PLAYER_START_X
from enemy import Enemy
from laser import Laser

pygame.mixer.init()

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
ENEMY_COUNT = 6
MAX_SCORE = 20


def is_player_collision(ex, ey, px, py):
    distance = math.sqrt((ex - px) ** 2 + (ey - py) ** 2)
    return distance < 57


def is_collision(ex, ey, lx, ly):
    distance = math.sqrt((ex - lx) ** 2 + (ey - ly) ** 2)
    return distance < 43


def quit():
    pygame.mixer.stop()


class GameMechanics:
    def __init__(self):
        self.score = 0
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pew Pew")
        #Images
        self.background = pygame.image.load('pictures_sounds/background.png')
        self.icon = pygame.image.load("pictures_sounds/rocket_icon.png")
        pygame.display.set_icon(self.icon)
        #Fonts
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)
        self.input_font = pygame.font.Font(None, 48)
        #Sounds
        self.background_music = pygame.mixer.Sound('pictures_sounds/sound.mp3')
        self.laser_sound = pygame.mixer.Sound('pictures_sounds/laser_sound.mp3')
        self.background_music.play(-1)  # -1 means loop indefinitely

        self.player = Player('pictures_sounds/rocket_shooting.png')
        self.laser = Laser('pictures_sounds/laser.png')
        self.enemies = [Enemy('pictures_sounds/thanos.png', SCREEN_WIDTH) for _ in range(ENEMY_COUNT)]

        self.reset_game()
        self.game_state = "menu"
        self.start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)
        self.instructions_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 120, 200, 50)
        self.back_button = pygame.Rect(50, SCREEN_HEIGHT - 70, 100, 50)
        self.restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)
        self.play_again_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 150, 200, 50)

        # Player name input
        self.player_name = ""
        self.input_box = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2, 400, 50)
        self.active = False
        self.error_message = ""
        self.leaderboard = self.load_leaderboard()

    def reset_game(self):
        self.score = 0
        self.player.x = PLAYER_START_X
        self.player.y = PLAYER_START_Y
        self.player.dx = 0

        self.enemies = [Enemy('pictures_sounds/thanos.png', SCREEN_WIDTH) for _ in range(ENEMY_COUNT)]
        self.laser.state = "ready"

    def draw_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def draw_button(self, button, text):
        pygame.draw.rect(self.screen, (0, 255, 0), button)
        button_text = self.font.render(text, True, (0, 0, 0))
        text_rect = button_text.get_rect(center=button.center)
        self.screen.blit(button_text, text_rect)

    def draw_menu(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        title_text = self.large_font.render("Pew Pew", True, (255, 255, 255))
        self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))
        self.draw_button(self.start_button, "Start Game")
        self.draw_button(self.instructions_button, "Instructions")

    def draw_instructions(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))

        title_text = self.large_font.render("Instructions", True, (255, 255, 255))
        self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))
        instructions = [
            "Use LEFT and RIGHT arrow keys to move",
            "Press SPACE to shoot",
            "Hit enemies to score points",
            "Press ESC to quit"
        ]
        for i, instruction in enumerate(instructions):
            text = self.font.render(instruction, True, (255, 255, 255))
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 250 + i * 40))

        # Back button
        self.draw_button(self.back_button, "Back")

    def draw_name_input(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        prompt_text = self.large_font.render("Enter your name:", True, (255, 255, 255))
        self.screen.blit(prompt_text, (SCREEN_WIDTH // 2 - prompt_text.get_width() // 2, 100))

        pygame.draw.rect(self.screen, (255, 255, 255), self.input_box, 2)
        name_text = self.input_font.render(self.player_name, True, (255, 255, 255))
        self.screen.blit(name_text, (self.input_box.x + 10, self.input_box.y + 10))

        if self.error_message:
            error_text = self.font.render(self.error_message, True, (255, 0, 0))
            self.screen.blit(error_text, (SCREEN_WIDTH // 2 - error_text.get_width() // 2, self.input_box.y + 70))

    def draw_game_over(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        game_over_text = self.large_font.render("Game Over", True, (255, 255, 255))
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 100))

        score_text = self.font.render(f"Final Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 250))
        self.draw_leaderboard()
        self.draw_button(self.play_again_button, "Play Again")

    def draw_leaderboard(self):
        leaderboard_title = self.font.render("Leaderboard", True, (255, 255, 255))
        self.screen.blit(leaderboard_title, (SCREEN_WIDTH // 2 - leaderboard_title.get_width() // 2, 350))

        for i, entry in enumerate(self.leaderboard):
            entry_text = self.font.render(f"{entry['player_name']}: {entry['score']}", True, (255, 255, 255))
            self.screen.blit(entry_text, (SCREEN_WIDTH // 2 - entry_text.get_width() // 2, 400 + i * 30))

    def update(self):
        if self.game_state == "menu":
            self.draw_menu()
        elif self.game_state == "instructions":
            self.draw_instructions()
        elif self.game_state == "input_name":
            self.draw_name_input()
        elif self.game_state == "playing":
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.background, (0, 0))

            self.player.update_position(SCREEN_WIDTH)

            for enemy in self.enemies:
                enemy.update_position(SCREEN_WIDTH)
                if is_collision(enemy.x, enemy.y, self.laser.x, self.laser.y):
                    self.laser.y = PLAYER_START_Y
                    self.laser.state = "ready"
                    self.score += 1
                    enemy.x = random.randint(0, SCREEN_WIDTH - 130)
                    enemy.y = random.randint(10, 150)

                    if self.score >= MAX_SCORE:
                        self.game_state = "game_over"
                        self.save_score()

                if enemy.y >= SCREEN_HEIGHT - 100 or is_player_collision(enemy.x, enemy.y, self.player.x, self.player.y - 50):
                    self.game_state = "game_over"
                    self.save_score()

                enemy.draw(self.screen)

            self.laser.update_position()

            self.laser.draw(self.screen)

            self.player.draw(self.screen)

            self.draw_score()
        elif self.game_state == "game_over":
            self.draw_game_over()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.game_state == "menu":
                if self.start_button.collidepoint(event.pos):
                    self.game_state = "input_name"
                elif self.instructions_button.collidepoint(event.pos):
                    self.game_state = "instructions"
            elif self.game_state == "instructions":
                if self.back_button.collidepoint(event.pos):
                    self.game_state = "menu"
            elif self.game_state == "game_over":
                if self.restart_button.collidepoint(event.pos):
                    self.game_state = "menu"
                elif self.play_again_button.collidepoint(event.pos):
                    self.reset_game()
                    self.game_state = "playing"
        elif event.type == pygame.KEYDOWN:
            if self.game_state == "input_name":
                if event.key == pygame.K_RETURN:
                    if 0 < len(self.player_name) <= 10:
                        self.game_state = "playing"
                        self.reset_game()
                    else:
                        self.error_message = "Name must be 1-10 characters long, letters and numbers only."
                elif event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                else:
                    self.player_name += event.unicode
            elif self.game_state == "playing":
                if event.key == pygame.K_LEFT:
                    self.player.move_left()
                elif event.key == pygame.K_RIGHT:
                    self.player.move_right()
                elif event.key == pygame.K_SPACE and self.laser.state == "ready":
                    self.laser.fire(self.player.x)
                    self.laser_sound.play()  # Play laser sound effect only when firing
        elif event.type == pygame.KEYUP:
            if self.game_state == "playing":
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    self.player.stop()

    def save_score(self):
        try:
            score = {"player_name": self.player_name, "score": self.score}
            self.leaderboard.append(score)
            self.leaderboard.sort(key=lambda x: x["score"], reverse=True)
            self.leaderboard = self.leaderboard[:10]  # Keep only top 10 scores

            with open('leaderboard.json', 'w') as f:
                json.dump(self.leaderboard, f)
        except Exception as e:
            print(f"An error occurred while saving the score: {e}")

    def load_leaderboard(self):
        try:
            with open('leaderboard.json', 'r') as f:
                json.dump(self.leaderboard, f, indent=4)
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"An error occurred while loading the leaderboard: {e}")
            return []



