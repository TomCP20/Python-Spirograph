# Spirograph

 A program that draws a randomly generated Spirographs via the turtle library.

![Spirograph](/Screenshots/001.png)

## How to run

This program was made using python version 3.12.1, pillow version 10.3.0 and several built in modules.

When run the program will draw a spirograph, when the spirograph is complete the user can do three things:

1. Left mouse click the turtle window to generate a new spirograph.
2. Middle mouse click the turtle window to save a gif of the creation of the spirograph (if enabled in config).
3. Right mouse click the turtle window to save a screenshot of the canvas.

To exit the program close the turtle window.

## configuration

### resolution

The number of steps taken to draw the spirograph, increasing makes the spirograph smoother but take londer to draw.

### size

The radius of the spirograph.

### create_gif

Controls whether the user can create a gif, enabling this makes the program run much slower.

### arms

The number of "arms" used to dram the spirograph, increasing results in more complex, less symetrical spirographs.
