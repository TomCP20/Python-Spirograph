from math import pi, cos, sin
from turtle import Turtle
from colorsys import hsv_to_rgb

resolution = 360
angleUnit = 2 * pi / resolution
angleDelta1 = 1 * angleUnit
angleDelta2 = 20 * angleUnit

r1 = 200
r2 = 180

turtle = Turtle()
turtle.screen.bgcolor("black")
turtle.hideturtle()
turtle.speed(0)

turtle.teleport(r1 + r2, 0)
for i in range(resolution+1):
    turtle.pencolor(hsv_to_rgb(i/resolution, 0.75, 0.75))
    x1 = cos(i * angleDelta1) * r1
    y1 = sin(i * angleDelta1) * r1

    x2 = x1 + cos(i * angleDelta2) * r2
    y2 = y1 + sin(i * angleDelta2) * r2

    turtle.setpos(x2, y2)


turtle.screen.mainloop()