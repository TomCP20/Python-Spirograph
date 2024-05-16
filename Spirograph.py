from math import pi, cos, sin, gcd
from turtle import Turtle
from colorsys import hsv_to_rgb
from random import randint

turtle = Turtle()
turtle.screen.bgcolor("black")
turtle.hideturtle()
turtle.speed(0)

resolution = 360
angleUnit = 2 * pi / resolution


def random_spirograph():
    angle_delta_1 = randint(1, 20)
    angle_delta_2 = randint(-20, 20)
    factor = gcd(angle_delta_1, angle_delta_2)
    angle_delta_1 = angle_delta_1//factor
    angle_delta_2 = angle_delta_2//factor

    r1 = randint(50, 200)
    r2 = randint(50, 200)

    spirograph(angle_delta_1, angle_delta_2, r1, r2)

def spirograph(angle_delta_1, angle_delta_2, r1, r2):
    turtle.teleport(r1 + r2, 0)
    for i in range(resolution+1):
        x2, y2 = step(angle_delta_1, angle_delta_2, r1, r2, i)

        turtle.setpos(x2, y2)

def step(angle_delta_1, angle_delta_2, r1, r2, i):
    turtle.pencolor(hsv_to_rgb(i/resolution, 0.75, 0.75))
    x1 = cos(i * angle_delta_1 * angleUnit) * r1
    y1 = sin(i * angle_delta_1 * angleUnit) * r1

    x2 = x1 + cos(i * angle_delta_2 * angleUnit) * r2
    y2 = y1 + sin(i * angle_delta_2 * angleUnit) * r2
    return x2,y2

random_spirograph()


turtle.screen.mainloop()