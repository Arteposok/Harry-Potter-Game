import pygame as pg
from os import path
import csv


class Sprite:
    def __init__(self, sur, x, y, w, h, **kw):
        self.win = sur
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.dir = path.join(path.dirname(__file__), "images")
        self.path = kw["path"]
        self.img = pg.image.load(path.join(self.dir, self.path)).convert()
        self.img = pg.transform.scale(self.img, (self.w, self.h))
        self.rect = None

    def draw(self):
        self.rect = self.img.get_rect(x=self.x, y=self.y)
        self.win.blit(self.img, self.rect)

    def move(self, x, y):
        self.x += x
        self.y += y


class TileLoader:
    def __init__(self, filepath):
        self.file_path = filepath
        self.file = open(filepath)
        self.card = list(csv.reader(self.file))
        self.worked_card = [["" for j in range(len(self.card[i]))] for i in range(len(self.card))]

    def get_card(self):
        return self.card

    def parse(self):
        for x in range(len(self.card) - 1):
            for y in range(len(self.card[x]) - 1):
                print(x)
                item = int(self.card[x][y])
                if item == -1:
                    self.worked_card[x][y] = "m"
                if item == 0:
                    self.worked_card[x][y] = "d"
                elif item == 2:
                    self.worked_card[x][y] = "g"
                elif item == 4:
                    self.worked_card[x][y] = "p"
                elif item == 5:
                    self.worked_card[x][y] = "w"
                elif item == 6:
                    self.worked_card[x][y] = "b"
                elif item == 7:
                    self.worked_card[x][y] = "o"
                elif item == 8 or item == 9:
                    self.worked_card[x][y] = "s"
                elif item == 10:
                    self.worked_card[x][y] = "1"
                elif item == 11:
                    self.worked_card[x][y] = "2"
                elif item == 12:
                    self.worked_card[x][y] = "3"
                elif item == 13:
                    self.worked_card[x][y] = "c"

        return self.worked_card


class TileAdapter:
    def __init__(self, surface, tilemap):
        self.tilemap = tilemap
        self.win = surface
        self.processed = [["" for j in range(len(self.tilemap[i]) - 1)] for i in range(len(self.tilemap) - 1)]
        self.size = 50

    def process(self):
        for x in range(len(self.tilemap) - 1):
            for y in range(len(self.tilemap[x]) - 1):
                item = self.tilemap[y][x]
                if item == "m":
                    self.processed[x][y] = Sprite(self.win, x * self.size, y * self.size, self.size, self.size,
                                                  path="dirt.jpg")
                if item == "d":
                    self.processed[x][y] = Sprite(self.win, x * self.size, y * self.size, self.size, self.size,
                                                  path="dirt.jpg")
                elif item == "g":
                    self.processed[x][y] = Sprite(self.win, x * self.size, y * self.size, self.size, self.size,
                                                  path="garden.jpg")
                elif item == "p":
                    self.processed[x][y] = Sprite(self.win, x * self.size, y * self.size, self.size, self.size,
                                                  path="planks.jpg")
                elif item == "w":
                    self.processed[x][y] = Sprite(self.win, x * self.size, y * self.size, self.size, self.size,
                                                  path="water.jpg")
                elif item == "b":
                    self.processed[x][y] = Sprite(self.win, x * self.size, y * self.size, self.size, self.size,
                                                  path="brick.jpg")
                elif item == "o":
                    self.processed[x][y] = Sprite(self.win, x * self.size, y * self.size, self.size, self.size,
                                                  path="goblet.jpg")
                elif item == "s":
                    self.processed[x][y] = Sprite(self.win, x * self.size, y * self.size, self.size, self.size,
                                                  path="stone.jpg")
                elif item == "o":
                    self.processed[x][y] = Sprite(self.win, x * self.size, y * self.size, self.size, self.size,
                                                  path="goblet.jpg")
                elif item == "1":
                    self.processed[x][y] = Sprite(self.win, x * self.size, y * self.size, self.size, self.size,
                                                  path="stair.jpg")
                elif item == "2":
                    self.processed[x][y] = Sprite(self.win, x * self.size, y * self.size, self.size, self.size,
                                                  path="stair_op.jpg")
                elif item == "c":
                    self.processed[x][y] = Sprite(self.win, x * self.size, y * self.size, self.size, self.size,
                                                  path="spawn.jpg")
                elif item == "3":
                    self.processed[x][y] = Sprite(self.win, x * self.size, y * self.size, self.size, self.size,
                                                  path="dragon_egg.jpg")
                else:
                    print("___________________________")
                    print(self.processed[x][y])
                    print(x, y)
                    self.processed[x][y] = Sprite(self.win, x * self.size, y * self.size, self.size, self.size,
                                                  path="dragon_egg.jpg")
        return self.processed
