import pygame

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Paddle(pygame.sprite.Sprite):
    
    def __init__(self, width, height):

        super().__init__()

        self.width = width
        self.height = height

        brick_png = pygame.image.load("blocks/28-Breakout-Tiles.png")  # or .convert_alpha()
        brick_png = pygame.transform.scale(brick_png, (width, height))
        brick_png = brick_png.convert()

        self.image = pygame.Surface((width, height))
        self.image = self.image.convert()
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        self.rect = brick_png.get_rect()

        self.image.blit(brick_png, self.rect)
    
    def move_left(self, x):
        self.rect.x -= x
        
        if (self.rect.x < 0):
            self.rect.x = 0
        
    def move_right(self, x):
        self.rect.x += x

        if ((self.rect.x + self.width) > WINDOW_WIDTH):
            self.rect.x = WINDOW_WIDTH - self.width