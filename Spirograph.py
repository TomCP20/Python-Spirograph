"""Spirograph"""
from math import pi, cos, sin, gcd
from tkinter import Canvas, Tk
from turtle import RawTurtle
from colorsys import hsv_to_rgb
from random import randint
import logging
import configparser
import time
from typing import Callable

from PIL import ImageGrab, Image


logger: logging.Logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def reset(turtle: RawTurtle) -> None:
    """reset the turtle"""
    turtle.screen.clear()
    turtle.screen.bgcolor("black")
    turtle.hideturtle()
    turtle.speed(0)


def random_spirograph(
    root: Tk,
    turtle: RawTurtle,
    resolution: int,
    size: int,
    create_gif: bool,
    arms: int,
) -> list[Image.Image]:
    """draw a random spirograph"""
    angle_deltas = [randint(-20, 20) for _ in range(arms)]
    factor: int = gcd(*angle_deltas)
    angle_deltas = [angle_delta // factor for angle_delta in angle_deltas]

    rs = [randint(50, 200) for _ in range(arms)]
    scale: float = size / sum(rs)
    rs = [r * scale for r in rs]

    return spirograph(root, turtle, angle_deltas, rs, resolution, size, create_gif)


def spirograph(
    root: Tk,
    turtle: RawTurtle,
    angle_deltas: list[int],
    rs: list[float],
    resolution: int,
    size: int,
    create_gif: bool,
) -> list[Image.Image]:
    """draw a spirograph"""
    logger.debug("initiating spirograph")
    for i, angle_delta in enumerate(angle_deltas):
        logger.debug("angle delta %i: %i", i, angle_delta)
    for i, r in enumerate(rs):
        logger.debug("r %i: %f", i, r)
    images: list[Image.Image] = []
    turtle.teleport(size, 0)
    reset(turtle)
    for i in range(resolution + 1):
        turtle.pencolor(hsv_to_rgb(i / resolution, 0.75, 0.75))
        turtle.setpos(*step(angle_deltas, rs, i / resolution))
        if create_gif:
            images.append(screenshot(root))
    return images


def step(angle_deltas: list[int], rs: list[float], t: float) -> tuple[float, float]:
    """generates the next step for the turtle"""
    a: float = t * 2 * pi
    x: float = sum(
        cos(a * angle_delta) * r for (angle_delta, r) in zip(angle_deltas, rs)
    )
    y: float = sum(
        sin(a * angle_delta) * r for (angle_delta, r) in zip(angle_deltas, rs)
    )
    return x, y


def loop(
    root: Tk,
    turtle: RawTurtle,
    resolution: int,
    size: int,
    create_gif: bool,
    arms: int,
) -> Callable[[float, float], None]:
    """loops the spirograph on click"""
    def sub_loop(_x: float, _y: float) -> None:
        images = random_spirograph(root, turtle, resolution, size, create_gif, arms)
        if create_gif:
            turtle.screen.onclick(save_gif(images), btn=2)
        turtle.screen.onclick(save_img(root), btn=3)
        turtle.screen.onclick(loop(root, turtle, resolution, size, create_gif, arms))

    return sub_loop


def save_img(root: Tk) -> Callable[[float, float], None]:
    """saves a screenshot"""
    def sub_save_img(_x: float, _y: float) -> None:
        screenshot(root).save(f"imgs/{time.time()}.png")

    return sub_save_img


def save_gif(images: list[Image.Image]) -> Callable[[float, float], None]:
    """saves a gif"""
    def sub_save_gif(_x: float, _y: float):
        images[1].save(
            f"imgs/{time.time()}.gif",
            save_all=True,
            append_images=images[2:],
            optimize=False,
            fps=10,
            loop=0,
        )

    return sub_save_gif


def screenshot(root: Tk) -> Image.Image:
    """takes a screenshot"""
    x0 = root.winfo_rootx()
    y0 = root.winfo_rooty()
    x1 = x0 + root.winfo_width()
    y1 = y0 + root.winfo_height()
    return ImageGrab.grab(all_screens=True).crop((x0 + 2, y0 + 2, x1 - 2, y1 - 2))


def main():
    """main"""
    config = configparser.ConfigParser()

    config.read("config.ini")

    root: Tk = Tk()
    canvas: Canvas = Canvas(root, width=900, height=900)
    canvas.pack()

    turtle: RawTurtle = RawTurtle(canvas)

    resolution: int = int(config["Settings"]["resolution"])
    size: int = int(config["Settings"]["size"])
    arms: int = int(config["Settings"]["arms"])

    create_gif: bool = bool(config["Settings"]["create_gif"])

    loop(root, turtle, resolution, size, create_gif, arms)(0, 0)
    turtle.screen.mainloop()

if __name__ == "__main__":
    main()
