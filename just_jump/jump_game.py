from tkinter import *
import random
import time

screen = [640, 480]

# classes
class Ball:
    def __init__(self, canvas, screen, color, paddle):
        self.canvas = canvas
        self.paddle = paddle
        self.id = canvas.create_oval(10, 10, 30, 30, fill=color, outline=color)
        self.screen = screen
        self.canvas.move(self.id, self.screen[0] / 2 - 10, self.screen[1] / 2 - 100)

        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        random.shuffle(starts)
        self.y = starts[0]

        self.hitBottom = False

    def hit_pad(self, pos):
        padPos = self.canvas.coords(self.paddle.id)
        if pos[2] >= padPos[0] and pos[0] <= padPos[2]:
            if pos[3] >= padPos[1] and pos[3] <= padPos[3]:
                return True
        return False

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if self.hit_pad(pos) == True:
            self.paddle.score += 1
            print(self.paddle.score)
            if (self.paddle.leftSpeed >= 0.3) or (self.paddle.rightSpeed >= 0.3):
                self.y = -2
            elif (self.paddle.leftSpeed < 0.3) and (self.paddle.leftSpeed >= 0.1) or (self.paddle.rightSpeed < 0.3) and (self.paddle.rightSpeed >=0.1):
                self.y = -(abs(self.y) + 1)
            else:
                self.y = -(abs(self.y) + 3)
        if (pos[0] <= 0) or (pos[2] >= self.screen[0]):
            self.x = -self.x
        if pos[1] <= 0:
            self.y = -self.y
        if pos[3] >= self.screen[1]:
            self.hitBottom = True
        

class Paddle:
    def __init__(self, canvas, screen, color):
        self.canvas = canvas
        self.screen = screen
        
        self.leftTime = time.time()
        self.rightTime = time.time()
        self.leftSpeed = 0
        self.rightSpeed = 0
        self.score = 0
        
        self.id = canvas.create_rectangle(0, 0, 100, 20, fill=color, outline=color)
        self.canvas.move(self.id, 100, screen[1] - 50)
        
        self.x = 0

        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)

    def turn_left(self, evt):
        self.x = -30
        self.leftSpeed = time.time() - self.leftTime
        self.leftTime = time.time()

    def turn_right(self, evt):
        self.x = 30
        self.rightSpeed = time.time() - self.rightTime
        self.rightTime = time.time()

    def draw(self):
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 5
            self.canvas.move(self.id, self.x, 0)
        elif pos[2] >= self.screen[0]:
            self.x = -5
            self.canvas.move(self.id, self.x, 0)
        else:
            self.canvas.move(self.id, self.x, 0)
            self.x = 0

tk = Tk()
tk.title("Just Jump")
tk.resizable(0, 0)
tk.wm_attributes("-topmost",1)

canvas = Canvas(tk, width=screen[0], height=screen[1], bd=0, highlightthickness=0)
canvas.pack()

winText = canvas.create_text(screen[0]/2, screen[1]/2, text="You lose, dude!", font=('Helvetica', 20, 'bold'), state="hidden")

pad1 = Paddle(canvas, screen, 'blue')
ball1 = Ball(canvas, screen, 'red', pad1)

scoreText = canvas.create_text(screen[0]-20, 20, text=pad1.score, font=('Helvetica', 20, 'bold'))

tk.update()


def start(evt):
    while 1:
        if ball1.hitBottom == False:
            ball1.draw()
            pad1.draw()
            canvas.itemconfig(scoreText, text=pad1.score)
        else:
            time.sleep(2)
            canvas.itemconfig(winText, state='normal')
        tk.update_idletasks()
        tk.update()
        time.sleep(0.01)

canvas.bind_all('<Button-1>', start)
