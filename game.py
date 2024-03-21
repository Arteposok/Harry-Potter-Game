import pygame as pg
from os import path
import tilemap as tm
import random as rnd
from math import *

pg.init()
WIDTH = 500
HEIGHT = 500
running = True
win = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("harry potter game")
ALLOWED_ITEMS = ("dirt.jpg", "brick.jpg", "stone.jpg", "spawn.jpg", "dragon_egg.jpg", "goblet.jpg")
controls = []
counter = 2
lose = False
toggle_vhs = False


class Game:
    def __init__(self, surface):
        self.player = None
        self.do = lambda: 0
        self.win = surface
        self.clock = pg.time.Clock()
        self.fps = 30
        self.timed = 0
        self.maxtime = 120
        self.first_level_map = tm.TileLoader(path.join("res", "first_lavel.csv"))
        self.second_level_map = []
        self.third_level_map = tm.TileLoader(path.join("res", "level_file.csv"))
        self.background = tm.TileAdapter(self.win, self.first_level_map.parse()).process()
        self.xb = 0
        self.yb = 0
        self.time = 0
        self.debug_mode = False
        self.spells = {"e": "expeliarmus", "r": "rediculus", "t": "actio"}
        self.mobs = []
        self.current_level = 1
        self.setup_fl()

    def set_fps(self, fps):
        self.fps = fps

    def events(self, fun):
        self.do = fun

    def youwin(self):
        def do_stuff():
            global toggle_vhs
            toggle_vhs = True
            img = pg.image.load("images/huray.jpg").convert()
            img = pg.transform.scale(img, (200, 200))
            img.set_colorkey("black")
            heading = pg.font.SysFont("Arial", 50).render("Huray! You Win!", False, (40, 40, 40))
            achieve = pg.font.SysFont("Arial", 20).render(f"it took you {self.time} seconds to complete", False,
                                                          (255, 255, 40))
            rect = pg.Rect(0, 0, 500, 500)
            pg.draw.rect(self.win, (90, 90, 90), rect)
            win.blit(heading, (100, 100))
            win.blit(achieve, ((500 - achieve.get_width()) / 2, 180))
            win.blit(img, ((500 - img.get_width()) / 2, 250))

        self.draw_and_update = do_stuff

    def youlose(self):
        def do_stuff():
            global toggle_vhs
            toggle_vhs = True
            img = pg.image.load("images/youlose.jpg").convert()
            img = pg.transform.scale(img, (200, 200))
            img.set_colorkey("black")
            heading = pg.font.SysFont("Arial", 50).render("HAHAHA YOU LOSE", False, (40, 40, 40))
            rect = pg.Rect(0, 0, 500, 500)
            pg.draw.rect(self.win, (90, 90, 90), rect)
            win.blit(heading, ((500 - heading.get_width()) / 2, 100))
            win.blit(img, ((500 - img.get_width()) / 2, 250))

        self.draw_and_update = do_stuff

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
        text = pg.font.SysFont("Arial", 20, bold=True).render(f"time left: {self.maxtime - self.time}", False,
                                                              (255, 255, 0))
        self.win.blit(text, (400, 10))
        if self.timed % self.fps == 0:
            self.time += 1
            self.timed = 0
        if self.maxtime - self.time <= 0:
            self.youlose()
        self.timed += 1
        self.player.draw()
        self.do()
        self.clock.tick(self.fps)

    def setup_fl(self):
        self.background = tm.TileAdapter(self.win, self.first_level_map.parse()).process()
        self.current_level = 1
        for i in self.background:
            for sprite in i:
                try:
                    if sprite.path == "spawn.jpg":
                        self.move(-sprite.x + 233, -sprite.y + 233)
                except:
                    pass

    def setup_tl(self):
        self.background = tm.TileAdapter(self.win, self.third_level_map.parse()).process()
        self.current_level = 3
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
                    if sprite.x < x - 12.5 < sprite.x + sprite.w:
                        if sprite.y < y - 12.5 < sprite.y + sprite.h:
                            if not (sprite is None):
                                return sprite
                            else:
                                return Sprite(self.win, 0, 0, 50, 50, path="planks.jpg")
                except:
                    pass


class Sprite:
    def __init__(self, sur, x, y, w, h, **kw):
        if "holdable" in kw.keys():
            self.holdable = kw["holdable"]
        else:
            self.holdable = False
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


class Button:
    def __init__(self, par, x, y, w, h, text, event=lambda: 0, font_size=20, bold=False):
        self.onclick = event
        self.win = par.win
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = pg.font.SysFont("Arial", font_size, bold=bold).render(text, False, (75, 75, 75))
        self.rect = pg.Rect(x, y, w, h)
        self.col = (80, 80, 80)
        self.hitbox = pg.Rect(self.x - 5, self.y - 5, self.w + 10, self.h + 10)
        self.last_state = False

    def get_text_params(self):
        px = (self.w - self.text.get_width()) / 2
        py = (self.h - self.text.get_height()) / 2
        return pg.Rect(self.x + px, self.y + py, self.text.get_width(), self.text.get_height())

    def draw(self):
        self.hitbox = pg.Rect(self.x - 5, self.y - 5, self.w + 10, self.h + 10)
        pg.draw.rect(self.win, self.col, pg.Rect(self.x - 5, self.y - 5, self.w + 10, self.h + 10))
        pg.draw.rect(self.win, (140, 140, 140), pg.Rect(self.x, self.y, self.w, self.h))
        win.blit(self.text, self.get_text_params())
        if self.hitbox.collidepoint(pg.mouse.get_pos()):
            self.col = (110, 110, 110)
        else:
            self.col = (80, 80, 80)
        if self.hitbox.collidepoint(pg.mouse.get_pos()) and pg.mouse.get_pressed()[0]:
            if pg.mouse.get_pressed()[0] != self.last_state and pg.mouse.get_pressed()[0]:
                self.onclick()
                self.last_state = True
        if not pg.mouse.get_pressed()[0]:
            self.last_state = False

    def on_click(self, func):
        self.onclick = func


class Player(Sprite):
    def __init__(self, sur, x, y, w, h, **kw):
        super().__init__(sur, x, y, w, h, **kw)
        self.hold = ""
        self.hp = 10
        self.tick = 0
        self.tick_rate = 100
        self.img.set_colorkey(self.img.get_at((0, 0)))

    def draw(self):
        super().draw()
        if lose:
            return
        self.tick += 1
        if self.hp < 10:
            if self.tick % self.tick_rate == 0:
                self.hp += 1
        if self.hp <= 0:
            game.youlose()
        if self.hold != "":
            self.img.blit(self.hold.img, self.hold.img.get_rect(x=10, y=10))
        y = 10
        x = (500 - 100) / 2
        pg.draw.rect(self.win, (80, 80, 80), pg.Rect(x - 5, y - 5, 100 + 10, 20 + 10))
        pg.draw.rect(self.win, (255 - game.player.hp * 10, game.player.hp * 20, 80),
                     pg.Rect(x, y, game.player.hp * 10, 20))


class Mob(Sprite):
    def __init__(self, sur, x, y, w, h, path="spider.jpg"):
        super().__init__(sur, x, y, w, h, path=path)
        self.angle = 0
        self.tick = 0
        self.hp = 5
        self.killed = False
        self.tick_rate = game.fps

    def draw(self):
        if not self.killed:
            super().draw()
            self.do_update()

    def do_update(self):
        self.tick += 1
        self.tick_rate = game.fps / 2
        if self.hp <= 0:
            self.killed = True
        if not self.killed:
            x = floor(game.player.x - self.w / 2 - self.x)
            y = floor(game.player.y - self.h / 2 - self.y)
            self.x += x / 30
            self.y += y / 30
            if x > 20 and (y - 20 < 0 < y + 20):
                self.img = pg.transform.rotate(self.img, self.angle * -1)
                self.img = pg.transform.rotate(self.img, -90)
                self.angle = -90
            elif x < -20 and (y - 20 < 0 < y + 20):
                self.img = pg.transform.rotate(self.img, self.angle * -1)
                self.img = pg.transform.rotate(self.img, 90)
                self.angle = 90
            if y > 20 and (x - 20 < 0 < x + 20):
                self.img = pg.transform.rotate(self.img, self.angle * -1)
                self.img = pg.transform.rotate(self.img, 180)
                self.angle = 180
            elif y < -20 and (x - 20 < 0 < x + 20):
                self.img = pg.transform.rotate(self.img, self.angle * -1)
                self.img = pg.transform.rotate(self.img, 0)
                self.angle = 0
            else:
                pass
            if self.tick % self.tick_rate == 0:
                pl = game.player
                if self.x < pl.x - 12.5 < self.x + self.w:
                    if self.y < pl.y - 12.5 < self.y + self.w:
                        game.player.hp -= 1


class Dragon(Mob):
    def __init__(self, sur, x, y, w, h, path="dragon.jpg"):
        super().__init__(sur, x, y, w, h, path)
        self.img = pg.transform.rotate(self.img, 90)
        self.tick_rate = 5
        self.img.set_colorkey("white")


game = Game(win)
player = Player(win, 235, 235, 30, 30, path="harry.jpg")
game.player = player
test_button = Button(game, 10, 10, 70, 40, "vhs is off")


@test_button.on_click
def click():
    global toggle_vhs
    toggle_vhs = not toggle_vhs
    test_button.text = pg.font.SysFont("Arial", 20).render(f"vhs is {'on' if toggle_vhs else 'off'}", False,
                                                           (75, 75, 75))


# game.background.append([test_button])
controls.append(test_button)
angle = 0

list = [False for i in range(200)]
list.append(True)


@game.events
def check():
    global angle
    keys = pg.key.get_pressed()
    # events are being checked here
    bpath = "none"
    if keys[pg.K_w]:
        try:
            bpath = game.item_at(250, 250 - 10).path
        except:
            return
        if not (bpath in ALLOWED_ITEMS):
            return
        for x in game.background:
            for sprite in x:
                sprite.y += 10
                game.player.img = pg.transform.rotate(game.player.img, 360 - angle)
                game.player.img = pg.transform.rotate(game.player.img, 0)
                angle = 0
    if keys[pg.K_s]:
        try:
            bpath = game.item_at(250, 250 + 30).path
        except:
            return
        if not (bpath in ALLOWED_ITEMS):
            return
        for x in game.background:
            for sprite in x:
                sprite.y += -10
                game.player.img = pg.transform.rotate(game.player.img, 360 - angle)
                game.player.img = pg.transform.rotate(game.player.img, 180)
                angle = 180
    if keys[pg.K_a]:
        try:
            bpath = game.item_at(250 - 10, 250).path
        except:
            return
        if not (bpath in ALLOWED_ITEMS):
            return
        for x in game.background:
            for sprite in x:
                sprite.x += 10
                game.player.img = pg.transform.rotate(game.player.img, 360 - angle)
                game.player.img = pg.transform.rotate(game.player.img, 90)
                angle = 90
    if keys[pg.K_d]:
        try:
            bpath = game.item_at(250 + 30, 250).path
        except:
            return
        if not (bpath in ALLOWED_ITEMS):
            return
        for x in game.background:
            for sprite in x:
                sprite.x += -10
                game.player.img = pg.transform.rotate(game.player.img, 360 - angle)
                game.player.img = pg.transform.rotate(game.player.img, 270)
                angle = 270
    try:
        if game.item_at(250, 290).path == "dragon_egg.jpg":
            game.setup_tl()
        if game.item_at(250, 250).path == "goblet.jpg":
            game.youwin()
    except:
        pass


game.background.append([Dragon(win, 0, 0, 200, 200)])

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            break
        if event.type == pg.MOUSEBUTTONDOWN:
            thing = game.item_at(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
            try:
                thing.hp -= 1
            except:
                pass

    win.fill((255, 255, 255))
    game.draw_and_update()
    if toggle_vhs:
        for i in range(0, 500, 10):
            horizontal_line = pg.Surface((500, 2), pg.SRCALPHA)
            horizontal_line.fill((255, 255, 255, 6))
            win.blit(horizontal_line, (0, (i - counter % 2) + rnd.randint(0, 3)))
    for i in controls:
        i.draw()
    if rnd.choice(list):
        if game.current_level == 3:
            x = rnd.randint(int(game.background[0][0].x), int(game.background[-1][-1].x))
            y = rnd.randint(int(game.background[0][0].y), int(game.background[-1][-1].y))
            print(game.background[0][0].x, game.background[-1][-1].x)
            game.background.append([Mob(win, x, y, 50, 50)])
    counter += 1
    pg.display.flip()
pg.quit()
