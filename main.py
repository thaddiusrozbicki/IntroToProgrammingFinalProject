'An overhaul of my 2nd project, using sprites, a start screen, larger game, etc.'

# content from kids can code: http://kidscancode.org/blog/

# sources
# https://www.101computing.net/pong-tutorial-using-pygame-adding-a-bouncing-ball/


# import libraries and modules
# from platform import platform
from ast import Delete
import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint
import os
from math import *
import time
from time import *

vec = pg.math.Vector2

# # game settings 
WIDTH = 360
HEIGHT = 480
FPS = 40
mpos = (0,0)

# player settings
PLAYER_GRAV = 0.9
PLAYER_FRIC = 0.1
SCORE = 0

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
# draws the text that will appear on screen once ran
def draw_text(text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)

def colorbyte():
    return random.randint(0,255)

# create all classees as sprites...

# player sprite, setting all ideas of Player, including color, velocity, health, etc
class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pg.Surface((100, 25))
        self.r = 0
        self.g = 0
        self.b = 255
        self.image.fill((self.r,self.g,self.b))
        self.rect = self.image.get_rect()
    
        self.pos = vec(WIDTH/2, HEIGHT)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.health = 100
#allows for control of player through keys using built in pygame functions 
    def controls(self):
        keys = pg.key.get_pressed()
        # if keys[pg.K_w]:
        #     self.acc.y = -5
        if keys[pg.K_a]:
            self.acc.x = -5
        # if keys[pg.K_s]:
        #     self.acc.y = 5
        if keys[pg.K_d]:
            self.acc.x = 5
    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, all_plats, False)
        self.rect.x += -1
        if hits:
            self.vel.y = -25
    def draw(self):
        pass
    def inbounds(self):
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
# updates the player with gravity,friction, and velocity
    def update(self):
        self.acc = vec(0,PLAYER_GRAV)
        self.controls()
        # friction
        self.acc.x += self.vel.x * -0.1
        # self.acc.y += self.vel.y * -0.1
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # self.rect.x += self.xvel
        # self.rect.y += self.yvel
        self.inbounds()
        self.rect.midbottom = self.pos

# platforms, sets their x and y values along with color
class Platform(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Ball class, where velocity,color,coordinates, and is drawn
class Ball(Sprite):
    def __init__(self, x, y, w, h, color):
        Sprite.__init__(self)
        self.color = color
        self.image = pg.Surface((w, h))
        self.image.fill(WHITE)
        self.velocity = [randint(4,8),randint(-8,8)]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
        self.yvel = 5
        self.xvel = 5
        pg.draw.rect(self.image, color, [HEIGHT/2, WIDTH/2, 8, 8])

# updating the ball with its velocites in both directions, and keeping it inbounds within the screen
    def update(self):
        self.rect.x += self.xvel
        self.rect.y += self.yvel
        if self.rect.x < 0:
            self.xvel*=-1
        if self.rect.y < 0:
            self.yvel*=-1
        if self.rect.x > WIDTH - self.rect.width:
            self.xvel*=-1
        if self.rect.y > HEIGHT - self.rect.height:
            self.yvel*=-1
#defines the bounce function and how it interacts when colliding with other objects 
    def bounce(self):
        self.xvel = -self.xvel
        self.yvel = randint(-8,8)
#defines the class mob as a subclass of sprite with coordinats,size,color,etc
class Mob(Sprite):
    def __init__(self, x, y, w, h, color, typeof, health):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.color = color
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.typeof = typeof
        self.initialized = False
        
    def init(self):
        self.initialized = True

    def update(self):
        self.rect.x += self.speed
        if self.typeof == "boss":
            if self.rect.right > WIDTH or self.rect.x < 0:
                self.speed *= -1
                self.rect.y += 15
        else:
            if self.rect.right > WIDTH or self.rect.x < 0:
                self.speed *= -1
     
# init pygame and create a window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My Game...")
clock = pg.time.Clock()

# instantiate classes
player = Player()
ground = Platform(0, HEIGHT, WIDTH, 1)
ball1 = Ball(50,250,25,25,RED)
roof = Platform(0,75,WIDTH, 1)
# create groups
all_sprites = pg.sprite.Group()
all_plats = pg.sprite.Group()
mobs = pg.sprite.Group()

# instantiate lots of mobs in a for loop and add them to groups
for i in range(15):
    m = Mob(randint(0,WIDTH-100), randint(75,HEIGHT/2), 75, 25, (colorbyte(),colorbyte(),colorbyte()), "normal", 5)
    all_sprites.add(m)
    mobs.add(m)
    m.init()
    print(m)

# add things to groups...
all_sprites.add(player, ground, ball1, roof)
all_plats.add(ground)

# Game loop
start_ticks = pg.time.get_ticks()
running = True
while running:
    # keep the loop running using clock
    delta = clock.tick(FPS)
    seconds = floor((pg.time.get_ticks()-start_ticks)/1000)
# checks for collison of floor and player and sets player y vel to 0 if so
    if pg.sprite.spritecollide(player, all_plats, False):
        player.pos.y = pg.sprite.spritecollide(player, all_plats, False)[0].rect.top
        player.vel.y = 0
# checks for balls collison with player and mobs, aka floating platforms, if colliding, uses bounce function as interaction
    if pg.sprite.collide_mask(ball1, player):
        ball1.bounce()
    if pg.sprite.collide_mask(ball1, roof):
        ball1.bounce()
    if pg.sprite.spritecollide(ball1, mobs,True):
        ball1.bounce()
    # checks for if player quit
    for event in pg.event.get():
        # check for closed window
        if event.type == pg.QUIT:
            running = False
    if pg.sprite.spritecollide(ball1, mobs, True):
        SCORE+=1
    if pg.sprite.collide_mask(ball1, ground):
        pg.quit()
    if len(mobs)==0:
        pg.quit()

    ############ Update ##############
    # update all sprites
    all_sprites.update()

    ############ Draw ################
    # draw the background screen
      
    screen.fill(BLACK)
    # screen.fill(BLACK)

    # draw text
    draw_text("FPS: " + str(delta), 22, RED, 64, HEIGHT / 24)
    draw_text("Timer: " + str(seconds), 22, RED, 64, HEIGHT / 10)
    draw_text("POINTS: " + str(SCORE), 22, WHITE, WIDTH / 2, HEIGHT / 24)
  
    # draw player color
    player.image.fill((player.r,player.g,player.b))

    # draw all sprites
    all_sprites.draw(screen)

    # buffer - after drawing everything, flip display
    pg.display.update()
    pg.display.flip()

pg.quit()
