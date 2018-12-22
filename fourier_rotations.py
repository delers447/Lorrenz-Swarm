from tkinter import *
import time, math, random

width, height = 600, 600
depth = 4
scale = .5

root = Tk()
root.geometry(f"{width}x{height}")

def process_data(data, datum):
    #expected for the datum to be y value float
    new_list = []
    #if data[len(data)-1] > width:
    #    pass
    for i, y in enumerate(data):
        x = width//2 + 2*i + 10
        #print(f"x:{x}, y:{y}")
        new_list.append((x, y[1]))
    new_list.insert(0, (width/2,datum))
    return new_list

def gethex(n):
    number = random.randint(0, 16 ** n)
    hexed = list(hex(number))
    hexed.pop(0)
    hexed.pop(0)
    while(len(hexed) < 6):
        hexed = ['0'] + hexed
    return '#' + ''.join(hexed)

class Circle:
    def __init__(self, canvas, center, radius, level):
        self.center = center
        self.radius = radius
        self.level = level
        self.angle_v = .1 * self.level
        self.canvas = canvas
        self.angle = 0
        self.color = 'white' #gethex(6)
        self.end = [self.center[0] + self.radius*math.cos(self.angle), self.center[1] + self.radius*math.sin(self.angle)]
        self.line_id = self.canvas.create_line(self.center[0], self.center[1], self.end[0], self.end[1], fill=self.color)
        self.circle_id = self.canvas.create_oval(self.center[0]-self.radius, self.center[1]-self.radius,
                                        self.center[0]+self.radius, self.center[1]+self.radius, outline=self.color)
        new_level = self.level + 1
        if new_level <= depth:
            #print(new_level)
            self.child = Circle(self.canvas, self.end, self.radius*scale, new_level)
        if self.level == depth:
            self.red_line = self.canvas.create_line(self.end[0], self.end[1], width/2, self.end[1], fill='red')
            self.data = [(self.end[0], self.end[1])]
            #print(f"Data: {self.data}")
            self.series = self.canvas.create_line(0, 0, 1, 1)

    def draw(self):
        self.canvas.delete(self.line_id)
        self.canvas.delete(self.circle_id)
        self.line_id = self.canvas.create_line(self.center[0], self.center[1], self.end[0], self.end[1], fill=self.color)
        self.circle_id = self.canvas.create_oval(self.center[0]-self.radius, self.center[1]-self.radius,
                                        self.center[0]+self.radius, self.center[1]+self.radius, outline=self.color)

    def graph(self):
        self.canvas.delete(self.red_line)
        self.red_line = self.canvas.create_line(self.end[0], self.end[1], width/2, self.end[1], fill='red')
        self.data = process_data(self.data, self.end[1])
        #print(f"Data: {self.data}")
        flattened = [a for x in self.data for a in x]
        #print(*flattened)
        self.canvas.delete(self.series)
        self.series = self.canvas.create_line(*flattened, smooth=True, fill='green')

    def rotate(self):
        if self.level%2 == 0:
            self.angle += self.angle_v
        elif self.level%2 == 1:
            self.angle -= self.angle_v
        if self.angle > math.pi * 2:
            self.angle -= math.pi * 2
        elif self.angle < -math.pi * 2:
            self.angle += math.pi * 2
        dx = self.radius * math.cos(self.angle)
        dy = self.radius * math.sin(self.angle)
        self.end = [self.center[0] + dx, self.center[1] + dy]
        return dx, dy

    def update(self):
        dx, dy = self.rotate()
        self.draw()
        if self.level < depth:
            self.child.center[0] = self.end[0]
            self.child.center[1] = self.end[1]
            self.child.update()
        if self.level == depth:
            self.graph()


def main():
    canvas = Canvas(root, height=height, width=width, bg='black')
    canvas.pack()

    #rotating circles
    center = [width/4, height/2]
    circles = Circle(canvas, center, height/6, 1)
    #graph axis
    canvas.create_line(width/2, height/7, width/2, height*7/8, fill='white')
    canvas.create_line(width/2, height*7/8, width, height*7/8, fill='white')

    while True:
        circles.update()
        root.update_idletasks()
        root.update()
        time.sleep(.1)

main()
