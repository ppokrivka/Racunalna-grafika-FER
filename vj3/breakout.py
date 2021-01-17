import pygame
import random
import sys

from paddle import Paddle
from ball import Ball
from brick import Brick

pygame.init()

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

PADDLE_WIDTH = 120
PADDLE_HEIGHT = 15
PADDLE_COLOR = (10, 200, 150)
PADDLE_SPEED = 7

BALL_WIDTH = 20
BALL_HEIGHT = 20
BALL_COLOR = RED
BALL_RADIUS = 7

BRICK_WIDTH = 57
BRICK_HEIGHT = 20
BRICK_SPACE = 2.5

# SCORE_MUL = 10

SCORE = 0
LIVES = 3

RANDOM_BOUNCE_PROB = 0.1

MAX_BRICK_FIRE_BALL = 15

ROWS = 8
COLUMNS = 15

font = pygame.font.Font(None, 40)


# Window init
size = (WINDOW_WIDTH, WINDOW_HEIGHT)
window = pygame.display.set_mode(size, pygame.DOUBLEBUF)
pygame.display.set_caption("Breakout")

background_image = pygame.image.load("blocks/background.png")
background_image = pygame.transform.scale(background_image, size)
background_image = background_image.convert()
rect = background_image.get_rect()

window.blit(background_image, rect)


# Pause screen init
pause_screen_size = (200, 200)
pause_surface = pygame.Surface(pause_screen_size)
pause_surface.set_alpha(128)
pause_surface.fill(BLACK)
text = font.render("PAUSED", 1, WHITE)
pause_surface.blit(text, (20,10))

clock = pygame.time.Clock()

all_objects = pygame.sprite.Group()

# Add paddle object
paddle = Paddle(PADDLE_WIDTH, PADDLE_HEIGHT)
paddle.rect.x = 450
paddle.rect.y = 560
all_objects.add(paddle)

# Add ball object
ball = Ball(BALL_WIDTH, BALL_HEIGHT)
ball.rect.x = 500
ball.rect.y = 540
all_objects.add(ball)

# Load level
lvl_name = sys.argv[1]
lvl = open(lvl_name)
lvl_blocks = [[block for block in row.strip().split(' ')] for row in lvl.readlines()]
lvl.close()

all_bricks = pygame.sprite.Group()


y = 70
for j in range(ROWS):
    x = 35
    for i in range(COLUMNS):
        brick_type = int(lvl_blocks[j][i])
        if(brick_type == 0):
            x += (BRICK_WIDTH + 2 * BRICK_SPACE)
            continue
        brick = Brick(brick_type, BRICK_WIDTH, BRICK_HEIGHT)
        brick.rect.x = x
        brick.rect.y = y
        
        all_bricks.add(brick)
        all_objects.add(brick)

        x += (BRICK_WIDTH + 2 * BRICK_SPACE)

    y += (BRICK_HEIGHT + 2 * BRICK_SPACE)
    
start = False
playing = True

fire_ball = False
fire_ball_bricks = 0

while playing:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start = not start

    # window.fill(RED)
    window.blit(background_image, rect)
   
    if not start:
        text = font.render(f"Press SPACE to start/pause", 1, WHITE)
        window.blit(text, (320, 500))

    text = font.render(f"Score: {SCORE}", 1, WHITE)
    window.blit(text, (20,10))

    text = font.render(f"Lives: {LIVES}", 1, WHITE)
    window.blit(text, (800,10))

    if start:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move_left(PADDLE_SPEED)
        elif keys[pygame.K_RIGHT]:
            paddle.move_right(PADDLE_SPEED)
        
        all_objects.update()

        # wall bounderies
        if (ball.rect.x < 10 or ball.rect.x > 990): # left or right
            ball.speed_x = -ball.speed_x
        # if (ball.rect.x > 990):     # right
        #     ball.speed_x = -ball.speed_x
        if (ball.rect.y < 40): # up
            ball.speed_y = -ball.speed_y
        if (ball.rect.y > 600): # down
            LIVES -=1
            start = False
            ball.rect.x = 500
            ball.rect.y = 540
            paddle.rect.x = 450
            paddle.rect.y = 560

            ball.speed_x = random.randint(-4, 4)
            ball.speed_y = random.randint(-7, -4)

            paddle.kill()
            PADDLE_WIDTH = 120
            PADDLE_SPEED = 7
            paddle = Paddle(PADDLE_WIDTH, PADDLE_HEIGHT)
            paddle.rect.x = 450
            paddle.rect.y = 560
            all_objects.add(paddle)

            if LIVES == 0:
                text = font.render("GAME OVER!", 1, WHITE)
                window.blit(text, (400,300))
                text = font.render(f"Lives: {LIVES}", 1, WHITE)
                window.blit(text, (800,10))
                pygame.display.flip()
                pygame.time.wait(3000)
                playing = False
            

        # ball and paddle
        if pygame.sprite.collide_mask(ball, paddle):
            ball.speed_y = -ball.speed_y
            ball.random_bounce()

        # ball and bricks
        collision = pygame.sprite.spritecollide(ball, all_bricks, False)
        if fire_ball:
            fire_ball_bricks += len(collision)
        
        if fire_ball_bricks > MAX_BRICK_FIRE_BALL: fire_ball = False

        bounce = True # if ball hits 2 bricks next to each other
        for brick in collision:
            SCORE +=1
            
            if bounce and not fire_ball:
                if ((ball.rect.x) < (brick.rect.x) or ball.rect.x > (brick.rect.x + BRICK_WIDTH)): # left side or right side
                    ball.speed_x = -ball.speed_x
                
                if ((ball.rect.y) < brick.rect.y or ball.rect.y > (brick.rect.y + BRICK_HEIGHT/4)): # up or downs
                    ball.speed_y = -ball.speed_y
                
                ball.random_bounce()

                bounce = not bounce

            if brick.type == 2:

                fire_ball_bricks +=1

                new_brick = Brick(3, BRICK_WIDTH, BRICK_HEIGHT)
                new_brick.rect.x = brick.rect.x
                new_brick.rect.y = brick.rect.y
        
                all_bricks.add(new_brick)
                all_objects.add(new_brick)

            elif brick.type == 4:
                PADDLE_SPEED +=3
                if PADDLE_SPEED > 15:
                    PADDLE_SPEED = 15

            elif brick.type == 5:
                PADDLE_SPEED -=3
                if PADDLE_SPEED < 5:
                    PADDLE_SPEED = 5

            elif brick.type == 6:
                PADDLE_WIDTH += 20
                if PADDLE_WIDTH > 200: 
                    PADDLE_WIDTH = 200
                else:
                    new_paddle = Paddle(PADDLE_WIDTH, PADDLE_HEIGHT)
                    new_paddle.rect.x = paddle.rect.x - 10
                    new_paddle.rect.y = paddle.rect.y
                    all_objects.add(new_paddle)
                    paddle.kill()
                    paddle = new_paddle

            elif brick.type == 7:
                PADDLE_WIDTH -= 20
                if PADDLE_WIDTH < 40: 
                    PADDLE_WIDTH = 40
                else:
                    new_paddle = Paddle(PADDLE_WIDTH, PADDLE_HEIGHT)
                    new_paddle.rect.x = paddle.rect.x + 10
                    new_paddle.rect.y = paddle.rect.y
                    all_objects.add(new_paddle)
                    paddle.kill()
                    paddle = new_paddle

            elif brick.type == 8:
                fire_ball = True
                fire_ball_bricks = 0

            brick.kill()
            if len(all_bricks) == 0:
                text = font.render("YOU WON!", 1, WHITE)
                window.blit(text, (400,300))
                pygame.display.flip()
                pygame.time.wait(3000)
                playing = False

    #window.fill(BLACK)

    pygame.draw.line(window, WHITE, [0, 40], [1000, 40], 2)

    all_objects.draw(window)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
