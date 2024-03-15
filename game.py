import pygame as pg
from os import path
import tilemap as tm
import random as rnd

pg.init()
WIDTH = 500
HEIGHT = 500
running = True
win = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("harry potter game")
ALLOWED_ITEMS = ("dirt.jpg", "brick.jpg", "stone.jpg", "spawn.jpg", "dragon_egg.jpg", "goblet.jpg")
controls = []
counter = 2
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
        text = pg.font.SysFont("Arial", 20, bold=True).render(f"time left: {self.maxtime-self.time}", False, (255, 255, 0))
        self.win.blit(text, (400, 10))
        if self.timed % self.fps == 0:
            self.time += 1
            self.timed = 0
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

    def tile(self, x, y):
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
        for sprite in self.mobs:
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
        self.damage = rnd.randint(70, 100)
        self.img.set_colorkey(self.img.get_at((0, 0)))

    def spell(self, key, tile):
        match key:
            case "e":
                self.col = (100, 170, 190)
                self.lx = pg.mouse.get_pos()[0]
                self.ly = pg.mouse.get_pos()[1]

                pass
            case "r":
                pass
            case "t":
                pass

    def draw(self):
        super().draw()
        if self.hold != "":
            self.img.blit(self.hold.img, self.hold.img.get_rect(x=10, y=10))


class Mob(Sprite):
    def __init__(self, sur, x, y, w, h, **kw):
        super().__init__(sur, x, y, w, h, **kw)
        self.hold = ""
        self.damage = rnd.randint(50, 100)
        self.hp = rnd.randint(300, 500)
        self.img.set_colorkey(self.img.get_at((0, 0)))

    def spell(self, spell):
        pass

    def draw(self):
        super().draw()
        if self.hold != "":
            self.img.blit(self.hold.img, self.hold.img.get_rect(x=10, y=10))


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


@game.events
def check():
    global angle
    keys = pg.key.get_pressed()
    # events are being checked here
    bpath = "none"
    if keys[pg.K_UP]:
        try:
            bpath = game.item_at(250, 250 - 10).path
        except:
            return
        if not (bpath in ALLOWED_ITEMS):
            print(bpath)
            return
        for x in game.background:
            for sprite in x:
                sprite.y += 10
                game.player.img = pg.transform.rotate(game.player.img, 360 - angle)
                game.player.img = pg.transform.rotate(game.player.img, 0)
                angle = 0
    if keys[pg.K_DOWN]:
        try:
            bpath = game.item_at(250, 250 + 30).path
        except:
            return
        if not (bpath in ALLOWED_ITEMS):
            print(bpath)
            return
        for x in game.background:
            for sprite in x:
                sprite.y += -10
                game.player.img = pg.transform.rotate(game.player.img, 360 - angle)
                game.player.img = pg.transform.rotate(game.player.img, 180)
                angle = 180
    if keys[pg.K_LEFT]:
        try:
            bpath = game.item_at(250 - 10, 250).path
        except:
            return
        if not (bpath in ALLOWED_ITEMS):
            print(bpath)
            return
        for x in game.background:
            for sprite in x:
                sprite.x += 10
                game.player.img = pg.transform.rotate(game.player.img, 360 - angle)
                game.player.img = pg.transform.rotate(game.player.img, 90)
                angle = 90
    if keys[pg.K_RIGHT]:
        try:
            bpath = game.item_at(250 + 30, 250).path
        except:
            return
        if not (bpath in ALLOWED_ITEMS):
            print(bpath)
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
        spell_keys = list(game.spells.keys())
        if event.type == pg.KEYDOWN:
            print("fffffff")
            k = event.key
            item = game.tile(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])


# not used
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        spell_keys = list(game.spells.keys())
        if event.type == pg.KEYDOWN:
            print("clicked")
            k = event.key
            item = game.tile(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
            game.player.spell("e" if k == pg.K_e else "r" if k == pg.K_r else "t" if k == pg.K_t else "", item)
    win.fill((255, 255, 255))
    game.draw_and_update()
    if toggle_vhs:
        for i in range(0, 500, 10):
            horizontal_line = pg.Surface((500, 2), pg.SRCALPHA)
            horizontal_line.fill((255, 255, 255, 6))
            win.blit(horizontal_line, (0, (i - counter % 2) + rnd.randint(0, 3)))
    for i in controls:
        i.draw()
    counter += 1
    pg.display.flip()
pg.quit()
