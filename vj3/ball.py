import pygame
import random

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

RANDOM_BOUNCE_PROB = 0.1

BALL_COLOR = RED
BALL_RADIUS = 7

class Ball(pygame.sprite.Sprite):
    
    def __init__(self, width, height):

        super().__init__()

        self.width = width
        self.height = height

        self.image = pygame.Surface((width, height))
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.circle(self.image, BALL_COLOR, (10, 10), BALL_RADIUS)

        self.rect = self.image.get_rect()

        self.speed_x = random.randint(-4, 4)
        self.speed_y = random.randint(-7, -4)

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
    
    def random_bounce(self):
        if (random.random() < RANDOM_BOUNCE_PROB):
            self.speed_x = random.randint(-4,4)
            self.speed_y = random.randint(-7, -4)