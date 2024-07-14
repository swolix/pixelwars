#!venv/bin/python3
import math
import wledmx
import time
import random
from pprint import pprint

HOST = ('localhost', 21324)

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

class Field:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.pixels = []
        for i in range(self.height):
            self.pixels.append([])
            for j in range(self.width):
                self.pixels[-1].append(0.0)

    def __getitem__(self, pos):
        return self.pixels[pos[1]][pos[0]]
    
    def getpixel(self, pos):
        v = self[pos]
        if v < 0:
            return (int(-v * 255), 0, 0)
        else:
            return (0, 0, int(255 * v))

    def __setitem__(self, pos, v):
        self.pixels[pos[1]][pos[0]] = v

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.field = Field(4, 5)
        self.field[0, 0] = -1.0
        self.field[4, 3] = 1.0
        self.screen.send_image(self.field)

    def shoot(self, red_blue_n):
        md = None
        if red_blue_n:
            for x in range(self.field.width):
                for y in range(self.field.height):
                    if self.field[x, y] >= 0:
                        d = math.sqrt(x * x * 0.9 + y * y)
                        if md is None or d < md:
                            md = d
                            p = (x, y)
            self.field[p] = -1
        else:
            for x in range(self.field.width):
                for y in range(self.field.height):
                    if self.field[x, y] <= 0:
                        d = math.sqrt((4-x) * (4-x) *0.9 + (3-y) * (3-y))
                        if md is None or d < md:
                            md = d
                            p = (x, y)
            self.field[p] = 1
        self.screen.send_image(self.field)

        if self.field[0, 0] == 1: raise Exception("Blue won")
        if self.field[4, 3] == -1: raise Exception("Red won")


if __name__ == "__main__":
    game = Game(wledmx.WledSend(HOST))
    while True:
        time.sleep(0.2)
        game.shoot(round(random.uniform(0, 1)) == 1)
