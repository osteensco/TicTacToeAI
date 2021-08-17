import pygame
import random
from pygame.constants import KEYDOWN, QUIT
from pygame.time import Clock
pygame.init()


class Block:
    def __init__(self, x, y, color, health=10):
        self.x = x
        self.y = y
        self.color = color
        self.health = health

    def draw(self, window):
        pygame.draw.rect(window, self.color, rect=(self.x, self.y, 25, 25)), self.x, self.y

class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # self.mask =

    def draw(self, window):
        pygame.draw.rect(window, (20,20,20), rect=(self.x, self.y, 60, 15)), self.x, self.y


class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.fall = True
        # self.mask = 

    def draw(self, window):
        pygame.draw.rect(window, (20,20,20), rect=(self.x, self.y, 15, 15)), self.x, self.y


def redraw_window(objs, WINDOW):
    for obj in objs:
            obj.draw(WINDOW)
    pygame.display.update()


def play_game():
    WIDTH, HEIGHT = 1080, 650
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    fps = 60
    paddle_speed = 15
    objs = []
    balls = []
    ball = Ball(550, 500)
    paddle = Paddle(500, 600)
    objs.append(ball)
    balls.append(ball)
    objs.append(paddle)
    running = True
    while running:
        WINDOW.fill([60,60,255])
        clock.tick(fps)
        redraw_window(objs, WINDOW)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and paddle.x >= 1:
            paddle.x -= paddle_speed
        if keys[pygame.K_d] and paddle.x <= WIDTH - paddle.get_width():
            paddle.x += paddle_speed
        #account for shooting paddle here


play_game()