import pygame as pg
from os import path
import tilemap as tm

pg.init()
WIDTH = 500
HEIGHT = 500
running = True
win = pg.display.set_mode((WIDTH, HEIGHT))


class Game:
    def __init__(self, surface):
        self.player = None
        self.do = lambda: 0
        self.win = surface
        self.clock = pg.time.Clock()
        self.fps = 30
        self.first_level_map = tm.TileLoader(path.join("res", "first_lavel.csv"))
        self.second_level_map = []
        self.third_level_map = tm.TileLoader(path.join("res", "level_file.csv"))
        self.background = tm.TileAdapter(self.win, self.first_level_map.parse()).process()
        self.xb = 0
        self.yb = 0
        self.debug_mode = False
        self.setup_fl()

    def set_fps(self, fps):
        self.fps = fps

    def events(self, fun):
        self.do = fun

    def centered(self):
        try:
            for i in self.background:
                for sprite in i:
                    if sprite.x < 235 < sprite.x + sprite.w:
                        if sprite.y < 235 < sprite.y + sprite.h:
                            return sprite
        except:
            return Sprite(self.win, 0, 0, 50, 50, path="dirt.jpg")

    def draw_and_update(self):
        for x in self.background:
            for sprite in x:
                sprite.draw()
        self.player.draw()
        self.do()
        self.clock.tick(self.fps)

    def setup_fl(self):
        self.background = tm.TileAdapter(self.win, self.third_level_map.parse()).process()
        for i in self.background:
            for sprite in i:
                try:
                    if sprite.path == "spawn.jpg":
                        self.move(-sprite.x + 233, -sprite.y + 233)
                except:
                    pass

    def move(self, x, y):
        for i in self.background:
            for sprite in i:
                try:
                    sprite.x += x
                    sprite.y += y
                except:
                    pass

    def item_at(self, x, y):
        for i in self.background:
            for sprite in i:
                try:
                    if sprite.x < x < sprite.x + sprite.w:
                        if sprite.y < y < sprite.y + sprite.h:
                            return sprite
                except:
                    pass


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


class Player(Sprite):
    def __init__(self, sur, x, y, w, h, **kw):
        super().__init__(sur, x, y, w, h, **kw)
        self.img.set_colorkey(self.img.get_at((0, 0)))

    def spell(self, spell):
        pass


game = Game(win)
player = Player(win, 235, 235, 30, 30, path="harry.jpg")
game.player = player
angle = 0


@game.events
def check():
    global angle
    keys = pg.key.get_pressed()
    # events are being checked here
    if keys[pg.K_UP]:
        for x in game.background:
            for sprite in x:
                sprite.y += 10
                game.player.img = pg.transform.rotate(game.player.img, 360 - angle)
                game.player.img = pg.transform.rotate(game.player.img, 0)
                angle = 0
    if keys[pg.K_DOWN]:
        for x in game.background:
            for sprite in x:
                sprite.y += -10
                game.player.img = pg.transform.rotate(game.player.img, 360 - angle)
                game.player.img = pg.transform.rotate(game.player.img, 180)
                angle = 180
    if keys[pg.K_LEFT]:
        for x in game.background:
            for sprite in x:
                sprite.x += 10
                game.player.img = pg.transform.rotate(game.player.img, 360 - angle)
                game.player.img = pg.transform.rotate(game.player.img, 90)
                angle = 90
    if keys[pg.K_RIGHT]:
        for x in game.background:
            for sprite in x:
                sprite.x += -10
                game.player.img = pg.transform.rotate(game.player.img, 360 - angle)
                game.player.img = pg.transform.rotate(game.player.img, 270)
                angle = 270
    print(game.item_at(game.background[0][0].x+233, game.background[0][0].y+233).path)


# not used
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    win.fill((255, 255, 255))
    game.draw_and_update()
    pg.display.flip()
pg.quit()
