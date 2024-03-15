import pygame as pg
import random as rnd

pg.init()

win = pg.display.set_mode((600, 500))

pg.display.set_caption("welcome to the triwizard tournament")


class Button:
    def __init__(self, par, x, y, w, h, text, event=lambda: 0, font_size=20, bold=False):
        self.onclick = event
        self.win = par
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


title = pg.font.SysFont("Arial", 30, bold=True).render("The Goblet Of Fire", False, (255, 40, 50))
title = pg.transform.scale(title, (500, 100))
bth = Button(win, (600 - 190) / 2, 170, 190, 80, "play", font_size=35, bold=False)
symbol = pg.image.load("images/huray.jpg").convert()
symbol = pg.transform.scale(symbol, (200, 200))


@bth.on_click
def do():
    global running
    import game
    running = False


counter = 2
running = True
dirt = pg.image.load("images/dirt.jpg").convert()
dirt = pg.transform.scale(dirt, (600, 500))
while running:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            running = False
    win.blit(dirt, (0, 0))
    for i in range(0, 500, 10):
        horizontal_line = pg.Surface((600, 2), pg.SRCALPHA)
        horizontal_line.fill((255, 255, 255, 6))
        win.blit(horizontal_line, (0, i - counter % 4 + rnd.randint(0, 3)))
    counter += 1
    win.blit(title, ((600 - title.get_width()) / 2, 50))
    bth.draw()
    win.blit(symbol, ((600 - symbol.get_width()) / 2, 270))
    pg.display.flip()
pg.quit()
