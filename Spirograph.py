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
    
def random_spirograph(turtle: RawTurtle, screen: TurtleScreen, resolution: int, size: int, create_gif: bool, arms: int) -> list[Image.Image]:
    angle_deltas = [randint(-20, 20) for _ in range(arms)]
    factor: int = gcd(*angle_deltas)
    angle_deltas = [angle_delta//factor for angle_delta in angle_deltas]

    rs = [randint(50, 200) for _ in range(arms)]
    scale: float = size/sum(rs)
    rs = [r*scale for r in rs]

    return spirograph(turtle, screen, angle_deltas, rs, resolution, size, create_gif)

def spirograph(turtle: RawTurtle, screen: TurtleScreen, angle_deltas: list[int], rs: list[float], resolution: int, size: int, create_gif: bool) -> list[Image.Image]:
    logger.debug("initiating spirograph")
    for (i, angle_delta) in enumerate(angle_deltas):
        logger.debug(f"angle delta {i}: {angle_delta}")
    for (i, r) in enumerate(rs):
        logger.debug(f"r {i}: {r}")
    images: list[Image.Image] = []
    turtle.teleport(size, 0)
    reset(turtle, screen)
    for i in range(resolution+1):
        turtle.pencolor(hsv_to_rgb(i/resolution, 0.75, 0.75))
        turtle.setpos(*step(angle_deltas, rs, i/resolution))
        if create_gif:
            images.append(screenshot(root))
    return images

def step(angle_deltas: list[int], rs: list[float], t: float) -> tuple[float, float]:
    a: float = t * 2 * pi
    x: float = sum(cos(a * angle_delta) * r for (angle_delta, r) in zip(angle_deltas, rs))
    y: float = sum(sin(a * angle_delta) * r for (angle_delta, r) in zip(angle_deltas, rs))
    return x, y

def loop(root: Tk, turtle: RawTurtle, screen: TurtleScreen, resolution: int, size: int, create_gif: bool, arms: int) -> Callable[[float, float], None]:
    def sub_loop(x: float, y: float) -> None:
        images = random_spirograph(turtle, screen, resolution, size, create_gif, arms)
        if (create_gif):
            screen.onclick(save_gif(images), btn=2)
        screen.onclick(save_img(root), btn=3)
        screen.onclick(loop(root, turtle, screen, resolution, size, create_gif, arms))
    return sub_loop

def save_img(root: Tk) -> Callable[[float, float], None]:
    def sub_save_img(x: float, y: float) -> None:
        screenshot(root).save(f"imgs/{time.time()}.png")
    return sub_save_img

def save_gif(images: list[Image.Image]) -> Callable[[float, float], None]:
    def sub_save_gif(x: float, y: float):
        images[1].save(f"imgs/{time.time()}.gif", save_all=True, append_images=images[2:], optimize=False, fps=10, loop=0)
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
    arms: int = int(Config["Settings"]["arms"])

    create_gif: bool = bool(Config["Settings"]["create_gif"])

    loop(root, turtle, screen, resolution, size, create_gif, arms)(0, 0)
    screen.mainloop()