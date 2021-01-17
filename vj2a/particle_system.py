from pyglet.gl import *
from pyglet.window import mouse
from pyglet.window import key

import random

start_x, start_y = 500, 0
vx_0, vy_0 = 0, 0

num_particles_batch = 5

opacity_treshold = 50

speed_y = 0
spread_x = 0

smoke = pyglet.image.load("smoke.bmp")

batch = pyglet.graphics.Batch()
particles = []


class Particle:

    def __init__(self, batch):
        self.sprite = pyglet.sprite.Sprite(img=smoke, x=start_x, y=start_y, batch=batch)
        self.vx = random.uniform(-3,3)
        self.vy = random.uniform(1,8)
        self.sprite.scale = 0.2

config = pyglet.gl.Config(double_buffer=True)
window = pyglet.window.Window(width=1000, height=600, config=config)


@window.event
def on_draw():
    window.clear()
    batch.draw()

def update(dt):
    global particles
    for i in range(len(particles)-1, -1, -1):
        particle = particles[i]
        particle.sprite.x += particle.vx + spread_x
        particle.sprite.y += particle.vy + speed_y
        particle.sprite.opacity *=0.98
        # particle.sprite.scale = 0.2
        
        if(particle.sprite.opacity < opacity_treshold):
            particles.remove(particle)

    new_particles()

@window.event
def on_key_press(symbol, modifiers):
    global start_x, start_y, num_particles_batch, opacity_treshold, speed_y, spread_x
    if symbol == key.LEFT:
        start_x -= 15
    elif symbol == key.RIGHT:
        start_x += 15
    elif symbol == key.UP:
        start_y += 15
    elif symbol == key.DOWN:
        start_y -= 15

    elif symbol == key.NUM_ADD:
        num_particles_batch += 1
    elif symbol == key.NUM_SUBTRACT:
        num_particles_batch -= 1
        if num_particles_batch <= 0:
            num_particles_batch = 0

    elif symbol == key.O:
        opacity_treshold +=10
        if opacity_treshold >=255:
            opacity_treshold = 255
    elif symbol == key.P:
        opacity_treshold -=10
        if opacity_treshold <= 0:
            opacity_treshold = 0

    elif symbol == key.NUM_8:
        speed_y +=5
        if speed_y >=50:
            speed_y = 50
    elif symbol == key.NUM_2:
        speed_y -=5
        # if speed_y <= 1:
        #     speed_y = 1
    elif symbol == key.NUM_6:
        spread_x +=5
        # if spread_x >=255:
        #     spread_x = 255
    elif symbol == key.NUM_4:
        spread_x -=5
        # if spread_x <= 0:
        #     spread_x = 0

def new_particles():
    for i in range(num_particles_batch):
        particles.append(Particle(batch))

pyglet.clock.schedule_interval(update, 1/45.)

pyglet.app.run()
