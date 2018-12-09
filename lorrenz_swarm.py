from tkinter import *
import time, math, random


width, height = 800, 800
root = Tk()
root.geometry(f"{width}x{height}")

class particle:
    def __init__(self, canvas, x, y, z, dx, dy, dz, color='red', size=10):
        self.x, self.y, self.z = x, y, z
        self.dx, self.dy, self.dz = dy, dx, dz
        self.canvas = canvas
        self.id = canvas.create_oval(width/2 + x, height/2 + y, width/2 + x + size, height/2 + y + size, fill=color)
        self.counter = 0

    def move(self, dt=.01):
        sigma, roe, beta = 10, 28, 8/3

        self.dx = (sigma * (self.y - self.x)) * dt
        self.dy = (self.x * (roe - self.z) - self.y) * dt
        self.dz = (self.x * self.y - beta * self.z) * dt

        self.x += self.dx
        self.y += self.dy
        self.z += self.dz

        self.canvas.move(self.id, self.dx*10, self.dy*10)

    def check_speed(self):
        if abs(self.dx + self.dy + self.dz) < 0.01:
            return True

    def check_position(self):
        if abs(self.x) > 100:
            return True
        elif abs(self.y) > 100:
            return True
        elif abs(self.z) > 100:
            return True
        else:
            return False

def magnitude(x, y, z):
    return math.sqrt(x **2 + y ** 2 + z ** 2)

def gethex(n):
    number = random.randint(0, 16 ** n)
    hexed = list(hex(number))
    hexed.pop(0)
    hexed.pop(0)
    while(len(hexed) < 6):
        hexed = ['0'] + hexed
    return ''.join(hexed)

def new_p(canvas, lower_d=-100, upper_d=100, lower_v=-2, upper_v=2):
    x, y, z = random.uniform(lower_d, upper_d), random.uniform(lower_d, upper_d), random.uniform(lower_d, upper_d)
    dx, dy, dz = random.uniform(lower_v, upper_v), random.uniform(lower_v, upper_v), random.uniform(lower_v, upper_v)
    p_color = '#' + gethex(6)
    p = particle(canvas, x, y, z, dx, dy, dz, color=p_color)
    return p

def check_ps(canvas, ps):
    new_ps = list()
    for i, p in enumerate(ps):
        if p.check_speed():
            new_ps.append(new_p(canvas, -2, 2, -1, 1)) if len(ps) < 600 else 0
            print("New P!")
        if p.check_position():
            p_temp = ps.pop(i)
            canvas.delete(p_temp.id)
            del p_temp
            print("pop!")
    return ps + new_ps


def main():
    c = Canvas(root, height=height, width=width, bg="black")
    c.pack()
    ps = list()
    p1 = particle(c, .1, .1, .1, 1, 1, 1, 'orange')
    ps.append(p1)
    counter = 0

    while True:
        for p in ps:
            p.move()
            #print("Moved!")
        ps = check_ps(c, ps)

        root.update_idletasks()
        root.update()
        time.sleep(.01)

main()
