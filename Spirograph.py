import math as Math
import turtle as Turtle
from colorsys import hsv_to_rgb

resolution = 360
angleUnit = 2 * Math.pi / resolution
angleDelta1 = 1 * angleUnit
angleDelta2 = 20 * angleUnit

r1 = 200
r2 = 180


Turtle.bgcolor("black")

Turtle.hideturtle()
Turtle.speed(0)



Turtle.teleport(r1 + r2, 0)
for i in range(resolution+1):
    Turtle.pencolor(hsv_to_rgb(i/resolution, 0.75, 0.75))
    x1 = Math.cos(i * angleDelta1) * r1
    y1 = Math.sin(i * angleDelta1) * r1

    x2 = x1 + Math.cos(i * angleDelta2) * r2
    y2 = y1 + Math.sin(i * angleDelta2) * r2

    Turtle.setpos(x2, y2)


Turtle.mainloop()