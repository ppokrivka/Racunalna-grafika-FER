import pygame

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Brick(pygame.sprite.Sprite):
    
    def __init__(self, brick_type, width, height):

        super().__init__()

        self.type = brick_type
        self.width = width
        self.height = height

        if self.type == 1: # normal brick
            png = "blocks/27-Breakout-Tiles.png"
        elif self.type == 2: # double brick
            png = "blocks/17-Breakout-Tiles.png"
        elif self.type == 3: # double brick second hit
            png = "blocks/18-Breakout-Tiles.png"
        elif self.type == 4: # increase paddle speed
            png = "blocks/42-Breakout-Tiles.png"
        elif self.type == 5: # decrease paddle speed
            png = "blocks/41-Breakout-Tiles.png"
        elif self.type == 6: # increase paddle size
            png = "blocks/47-Breakout-Tiles.png"
        elif self.type == 7: # decrease paddle size
            png = "blocks/46-Breakout-Tiles.png"
        elif self.type == 8: # fire ball
            png = "blocks/44-Breakout-Tiles.png"
        
        brick_png = pygame.image.load(png)  # or .convert_alpha()
        brick_png = pygame.transform.scale(brick_png, (width, height))
        brick_png = brick_png.convert()
        
        self.image = pygame.Surface((width, height))
        self.image = self.image.convert()
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        self.rect = brick_png.get_rect()

        self.image.blit(brick_png, self.rect)