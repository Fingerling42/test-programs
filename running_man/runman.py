from tkinter import *
import random
import time

# Game classes

class Game:
    def __init__(self):
        self.tk = Tk()
        self.tk.title("Running Man")
        self.tk.resizable(0,0)
        self.tk.wm_attributes("-topmost", 1)
        self.cWidth = 600
        self.cHeight = 600
        self.canvas = Canvas(self.tk, width=self.cWidth, height=self.cHeight, highlightthickness=0)
        self.canvas.pack()
        self.tk.update()

        self.bg1 = PhotoImage(file="background.gif")
        self.bg2 = PhotoImage(file="background2.gif")
        bW = []
        bH = []
        bW.append(self.bg1.width())
        bH.append(self.bg1.height())
        bW.append(self.bg2.width())
        bH.append(self.bg2.height())
        for x in range(0, 3):
            for y in range(0, 3):
                if (y % 2 == 0 and x % 2 == 0) or (y % 2 == 1 and x % 2 == 1):
                    self.canvas.create_image(x * bW[0], y * bH[0], image=self.bg1, anchor='nw')
                else:
                    self.canvas.create_image(x * bW[1], y * bH[1], image=self.bg2, anchor='nw')

        self.sprites = []
        self.running = True

    def main_loop(self):
        while 1:
            if self.running == True:
                for sprite in self.sprites:
                    sprite.move()

            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.01)

class Coords:
    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

class Sprite:
    def __init__(self, game):
        self.game = game
        self.endgame = False
        self.coordinates = None

    def move(self):
        pass

    def coords(self):
        return self.coordinates

class Platform(Sprite):
    def __init__(self, game, photoImage, x, y, width, height):
        Sprite.__init__(self, game)
        self.photoImage = photoImage
        self.image = game.canvas.create_image(x,y, image=self.photoImage, anchor='nw')
        self.coordinates = Coords(x, y, x + width, y + height)

class Man(Sprite):
    def __init__(self, game):
        Sprite.__init__(self, game)
        self.imageLeft = [
            PhotoImage(file="man_stand_l.gif"),
            PhotoImage(file="man_run1_l.gif"),
            PhotoImage(file="man_run2_l.gif"),
            PhotoImage(file="man_jump_l.gif")
            ]
        self.imageRight = [
            PhotoImage(file="man_stand_r.gif"),
            PhotoImage(file="man_run1_r.gif"),
            PhotoImage(file="man_run2_r.gif"),
            PhotoImage(file="man_jump_r.gif")
            ]
        self.image = game.canvas.create_image(25, 500, image=self.imageRight[0], anchor='nw')

        self.x = 0
        self.y = 0
        self.currentImage = 0
        self.currentImageAdd = 1
        self.jumpCount = 0
        self.lastTime = time.time()
        self.coordinates = Coords()

        game.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        game.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        game.canvas.bind_all('<space>', self.jump)

    def turn_left(self, evt):
        if self.y == 0:
            self.x = -2

    def turn_right(self, evt):
        if self.y == 0:
            self.x = 2

    def jump(self, evt):
        if self.y == 0:
            self.y = -4
            self.jumpCount = 0

    def animate(self):
        if self.x != 0 and self.y == 0:
            if time.time() - self.lastTime > 0.1:
                self.lastTime = time.time()
                self.currentImage += self.currentImageAdd
                if self.currentImage >= 3:
                    self.currentImageAdd = -1
                if self.currentImage <= 1:
                    self.currentImageAdd = 1

        if self.x == 0 and self.y == 0:
            self.game.canvas.itemconfig(self.image, image=self.imageLeft[0])

        if self.x < 0:
            if self.y != 0:
                self.game.canvas.itemconfig(self.image, image=self.imageLeft[3])
            else:
                self.game.canvas.itemconfig(self.image, image=self.imageLeft[self.currentImage])
        elif self.x > 0:
            if self.y != 0:
                self.game.canvas.itemconfig(self.image, image=self.imageRight[3])
            else:
                self.game.canvas.itemconfig(self.image, image=self.imageRight[self.currentImage])

    def coords(self):
        xy = self.game.canvas.coords(self.image)
        self.coordinates.x1 = xy[0]
        self.coordinates.y1 = xy[1]
        self.coordinates.x2 = xy[0] + 50
        self.coordinates.y2 = xy[1] + 50
        return self.coordinates

    def move(self):
        self.animate()
        if self.y < 0:
            self.jumpCount += 1
            if self.jumpCount > 20:
                self.y = 4
        if self.y > 0:
            self.jumpCount -= 1

        co = self.coords()
        left = True
        right = True
        top = True
        bottom = True
        falling = True

        if self.y > 0 and co.y2 >= self.game.cHeight:
            self.y = 0
            bottom = False
        elif self.y < 0 and co.y1 <= 0:
            self.y = 0
            top = False

        if self.x > 0 and co.x2 >= self.game.cWidth:
            self.x = 0
            right = False
        elif self.x < 0 and co.x1 <=0:
            self.x = 0
            left = False

        for sprite in self.game.sprites:
            if sprite == self:
                continue
            spriteCo = sprite.coords()
            
            if top and self.y < 0 and col_top(co, spriteCo):
                self.y = -self.y
                top = False

            if bottom and self.y > 0 and col_bottom(self.y, co, spriteCo):
                self.y = spriteCo.y1 - co.y2
                if self.y < 0:
                    self.y = 0
                bottom = False
                top = False

            if bottom and falling and self.y == 0 and co.y2 < self.game.cHeight and col_bottom(1, co, spriteCo):
                falling = False

            if left and self.x < 0 and col_left(co, spriteCo):
                self.x = 0
                left = False
            if right and self.x > 0 and col_right(co, spriteCo):
                self.x = 0
                right = False

        if falling and bottom and self.y == 0 and co.y2 < self.game.cHeight:
            self.y = 4

        self.game.canvas.move(self.image, self.x, self.y)
        self.x = 0
        
# Functions

def within_x(co1, co2):
    if co1.x1 > co2.x1 and co1.x1 < co2.x2 \
       or co1.x2 > co2.x1 and co1.x2 < co2.x2 \
       or co2.x1 > co1.x1 and co2.x1 < co1.x2 \
       or co2.x2 > co1.x1 and co2.x2 < co1.x2:
        return True
    else:
        return False

def within_y(co1, co2):
    if (co1.y1 > co2.y1 and co1.y1 < co2.y2) \
       or (co1.y2 > co2.y1 and co1.y2 < co2.y2) \
       or (co2.y1 > co1.y1 and co2.y1 < co1.y2) \
       or (co2.y2 > co1.y1 and co2.y2 < co1.y2):
        return True
    else:
        return False

def col_left(co1, co2):
    if within_y(co1, co2):
        if co1.x1 <= co2.x2 and co1.x1 >= co2.x1:
            return True
    return False

def col_right(co1, co2):
    if within_y(co1, co2):
        if co1.x2 >= co2.x1 and co1.x2 <= co2.x2:
            return True
    return False

def col_top(co1, co2):
    if within_x(co1, co2):
        if co1.y1 <= co2.y2 and co1.y1 >= co2.y1:
            return True
    return False

def col_bottom(y, co1, co2):
    if within_x(co1, co2):
        yCalc = co1.y2 + y
        if yCalc >= co2.y1 and yCalc <= co2.y2:
            return True
    return False

# Start game
g = Game()

platform1 = Platform(g, PhotoImage(file="platform2.gif"), 0, 550, 100, 15)
g.sprites.append(platform1)

platform2 = Platform(g, PhotoImage(file="platform3.gif"), 120, 480, 150, 15)
g.sprites.append(platform2)

platform3 = Platform(g, PhotoImage(file="platform1.gif"), 330, 480, 60, 15)
g.sprites.append(platform3)

platform4 = Platform(g, PhotoImage(file="platform1.gif"), 450, 480, 60, 15)
g.sprites.append(platform4)

platform5 = Platform(g, PhotoImage(file="platform2.gif"), 500, 400, 100, 15)
g.sprites.append(platform5)

platform6 = Platform(g, PhotoImage(file="platform2.gif"), 320, 350, 100, 15)
g.sprites.append(platform6)

platform7 = Platform(g, PhotoImage(file="platform3.gif"), 100, 300, 150, 15)
g.sprites.append(platform7)

platform8 = Platform(g, PhotoImage(file="platform1.gif"), 20, 230, 60, 15)
g.sprites.append(platform8)

platform9 = Platform(g, PhotoImage(file="platform1.gif"), 120, 150, 60, 15)
g.sprites.append(platform9)

platform10 = Platform(g, PhotoImage(file="platform2.gif"), 190, 80, 100, 15)
g.sprites.append(platform10)

platform11 = Platform(g, PhotoImage(file="platform1.gif"), 300, 150, 60, 15)
g.sprites.append(platform11)

platform12 = Platform(g, PhotoImage(file="platform2.gif"), 420, 150, 100, 15)
g.sprites.append(platform12)

platform13 = Platform(g, PhotoImage(file="platform2.gif"), 500, 80, 100, 15)
g.sprites.append(platform13)

man = Man(g)
g.sprites.append(man)

g.main_loop()
