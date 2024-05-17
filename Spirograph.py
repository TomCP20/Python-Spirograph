from math import pi, cos, sin, gcd
from turtle import Turtle, Screen
from colorsys import hsv_to_rgb
from random import randint
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

screen = Screen()
turtle = Turtle()

resolution = 360
size = 390

def reset():
    screen.clear()
    screen.bgcolor("black")
    turtle.hideturtle()
    turtle.speed(0)
    
def random_spirograph():
    angle_delta_1 = randint(1, 20)
    angle_delta_2 = randint(-20, 20)
    while angle_delta_2 == 0 or angle_delta_1 == angle_delta_2:
        angle_delta_2 = randint(-20, 20)
    factor = gcd(angle_delta_1, angle_delta_2)
    angle_delta_1 //= factor
    angle_delta_2 //= factor

    r1 = randint(50, 200)
    r2 = randint(50, 200)
    sum_r = r1 + r2
    r1 *= size/sum_r
    r2 *= size/sum_r

    spirograph(angle_delta_1, angle_delta_2, r1, r2)

def spirograph(angle_delta_1, angle_delta_2, r1, r2):
    logger.debug("initiating spirograph")
    logger.debug(f"angle delta 1: {angle_delta_1}")
    logger.debug(f"angle delta 2: {angle_delta_2}")
    logger.debug(f"r 1: {r1}")
    logger.debug(f"r 2: {r2}")
    turtle.teleport(size, 0)
    reset()
    for i in range(resolution+1):
        x2, y2 = step(angle_delta_1, angle_delta_2, r1, r2, i/resolution)

        turtle.setpos(x2, y2)

def step(angle_delta_1, angle_delta_2, r1, r2, t):
    turtle.pencolor(hsv_to_rgb(t, 0.75, 0.75))
    x1 = cos(t * angle_delta_1 * 2 * pi) * r1
    y1 = sin(t * angle_delta_1 * 2 * pi) * r1

    x2 = x1 + cos(t * angle_delta_2 * 2 * pi) * r2
    y2 = y1 + sin(t * angle_delta_2 * 2 * pi) * r2
    return x2,y2

def loop(x, y):
    random_spirograph()
    screen.onclick(loop)

random_spirograph()
screen.onclick(loop)
screen.mainloop()
