from math import pi, cos, sin, gcd
from turtle import Turtle
from colorsys import hsv_to_rgb
from random import randint

resolution = 360
angleUnit = 2 * pi / resolution
angleDelta1 = randint(1, 20)
angleDelta2 = randint(-20, 20)
factor = gcd(angleDelta1, angleDelta2)
angleDelta1 = angleDelta1//factor
angleDelta2 = angleDelta2//factor

r1 = randint(50, 200)
r2 = randint(50, 200)

turtle = Turtle()
turtle.screen.bgcolor("black")
turtle.hideturtle()
turtle.speed(0)

turtle.teleport(r1 + r2, 0)
for i in range(resolution+1):
    turtle.pencolor(hsv_to_rgb(i/resolution, 0.75, 0.75))
    x1 = cos(i * angleDelta1 * angleUnit) * r1
    y1 = sin(i * angleDelta1 * angleUnit) * r1

    x2 = x1 + cos(i * angleDelta2 * angleUnit) * r2
    y2 = y1 + sin(i * angleDelta2 * angleUnit) * r2

    turtle.setpos(x2, y2)


turtle.screen.mainloop()