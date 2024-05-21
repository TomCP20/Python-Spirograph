from PIL import ImageGrab
from math import pi, cos, sin, gcd
from tkinter import Canvas, Tk
from turtle import RawTurtle, TurtleScreen
from colorsys import hsv_to_rgb
from random import randint
import logging
import time

logger: logging.Logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

root = Tk()
canvas = Canvas(root, width=900, height=900)
canvas.pack()

turtle: RawTurtle = RawTurtle(canvas)

screen: TurtleScreen = turtle.screen

resolution: int = 1000
size: int = 400

def reset() -> None:
    screen.clear()
    screen.bgcolor("black")
    turtle.hideturtle()
    turtle.speed(0)
    
def random_spirograph() -> None:
    angle_delta_1: int = randint(1, 20)
    angle_delta_2: int = randint(-20, 20)
    while angle_delta_2 == 0 or angle_delta_1 == angle_delta_2:
        angle_delta_2 = randint(-20, 20)
    factor: int = gcd(angle_delta_1, angle_delta_2)
    angle_delta_1 //= factor
    angle_delta_2 //= factor

    r1: float = randint(50, 200)
    r2: float = randint(50, 200)
    sum_r: float = r1 + r2
    r1 *= size/sum_r
    r2 *= size/sum_r

    spirograph(angle_delta_1, angle_delta_2, r1, r2)

def spirograph(angle_delta_1: int, angle_delta_2: int, r1: float, r2: float) -> None:
    logger.debug("initiating spirograph")
    logger.debug(f"angle delta 1: {angle_delta_1}")
    logger.debug(f"angle delta 2: {angle_delta_2}")
    logger.debug(f"r 1: {r1}")
    logger.debug(f"r 2: {r2}")
    turtle.teleport(size, 0)
    reset()
    for i in range(resolution+1):
        turtle.setpos(*step(angle_delta_1, angle_delta_2, r1, r2, i/resolution))

def step(angle_delta_1: int, angle_delta_2: int, r1: float, r2: float, t: float) -> tuple[float, float]:
    turtle.pencolor(hsv_to_rgb(t, 0.75, 0.75))
    a: float = t * 2 * pi

    x1: float = cos(a * angle_delta_1) * r1
    y1: float = sin(a * angle_delta_1) * r1

    x2: float = x1 + cos(a * angle_delta_2) * r2
    y2: float = y1 + sin(a * angle_delta_2) * r2
    return x2,y2

def loop(x: float, y: float) -> None:
    random_spirograph()
    screen.onclick(screenshot, btn=3)
    screen.onclick(loop)

def screenshot(x: float, y: float) -> None:
    x0 = root.winfo_rootx()
    y0 = root.winfo_rooty()
    x1 = x0 + root.winfo_width()
    y1 = y0 + root.winfo_height()
    ImageGrab.grab().crop((x0+2, y0+2, x1-2, y1-2)).save(f"imgs/{time.time()}.png")

loop(0, 0)
screen.mainloop()