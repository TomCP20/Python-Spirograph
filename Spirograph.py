import io
from PIL import ImageGrab, Image
from math import pi, cos, sin, gcd
from tkinter import Canvas, Tk
from turtle import RawTurtle, TurtleScreen
from colorsys import hsv_to_rgb
from random import randint
import logging
import configparser
import time
from typing import Callable

logger: logging.Logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)



def reset(turtle: RawTurtle, screen: TurtleScreen) -> None:
    screen.clear()
    screen.bgcolor("black")
    turtle.hideturtle()
    turtle.speed(0)
    
def random_spirograph(turtle: RawTurtle, screen: TurtleScreen, resolution: int, size: int, create_gif: bool) -> list[Image.Image]:
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

    return spirograph(turtle, screen, angle_delta_1, angle_delta_2, r1, r2, resolution, size, create_gif)

def spirograph(turtle: RawTurtle, screen: TurtleScreen, angle_delta_1: int, angle_delta_2: int, r1: float, r2: float, resolution: int, size: int, create_gif: bool) -> list[Image.Image]:
    logger.debug("initiating spirograph")
    logger.debug(f"angle delta 1: {angle_delta_1}")
    logger.debug(f"angle delta 2: {angle_delta_2}")
    logger.debug(f"r 1: {r1}")
    logger.debug(f"r 2: {r2}")
    images: list[Image.Image] = []
    turtle.teleport(size, 0)
    reset(turtle, screen)
    for i in range(resolution+1):
        turtle.pencolor(hsv_to_rgb(i/resolution, 0.75, 0.75))
        turtle.setpos(*step(angle_delta_1, angle_delta_2, r1, r2, i/resolution))
        if create_gif:
            images.append(screenshot(root))
    return images

def step(angle_delta_1: int, angle_delta_2: int, r1: float, r2: float, t: float) -> tuple[float, float]:
    
    a: float = t * 2 * pi

    x1: float = cos(a * angle_delta_1) * r1
    y1: float = sin(a * angle_delta_1) * r1

    x2: float = x1 + cos(a * angle_delta_2) * r2
    y2: float = y1 + sin(a * angle_delta_2) * r2
    return x2,y2

def loop(root: Tk, turtle: RawTurtle, screen: TurtleScreen, resolution: int, size: int, create_gif: bool) -> Callable[[float, float], None]:
    def sub_loop(x: float, y: float) -> None:
        images = random_spirograph(turtle, screen, resolution, size, create_gif)
        if (create_gif):
            screen.onclick(save_gif(images), btn=2)
        screen.onclick(save_img(root), btn=3)
        screen.onclick(loop(root, turtle, screen, resolution, size, create_gif))
    return sub_loop

def save_img(root: Tk) -> Callable[[float, float], None]:
    def sub_save_img(x: float, y: float) -> None:
        screenshot(root).save(f"imgs/{time.time()}.png")
    return sub_save_img

def save_gif(images: list[Image.Image]) -> Callable[[float, float], None]:
    def sub_save_gif(x: float, y: float):
        images[1].save(f"imgs/{time.time()}.gif", save_all=True, append_images=images[2:], optimize=False, duration=40, loop=0)
    return sub_save_gif


def screenshot(root: Tk) -> Image.Image:
    x0 = root.winfo_rootx()
    y0 = root.winfo_rooty()
    x1 = x0 + root.winfo_width()
    y1 = y0 + root.winfo_height()
    return ImageGrab.grab(all_screens=True).crop((x0+2, y0+2, x1-2, y1-2))

if __name__ == '__main__':


    Config = configparser.ConfigParser()

    Config.read("config.ini")


    root: Tk = Tk()
    canvas: Canvas = Canvas(root, width=900, height=900)
    canvas.pack()

    turtle: RawTurtle = RawTurtle(canvas)

    screen: TurtleScreen = turtle.screen

    resolution: int = int(Config["Settings"]["resolution"])
    size: int = int(Config["Settings"]["size"])

    create_gif: bool = bool(Config["Settings"]["create_gif"])

    loop(root, turtle, screen, resolution, size, create_gif)(0, 0)
    screen.mainloop()