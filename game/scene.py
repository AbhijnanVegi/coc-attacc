from colorama import init, Fore, Back, Style
import sys
import subprocess as sp
import numpy as np
import math

from game.game_object import GameObject


class Scene:
    def __init__(self, width, height):
        self.frame = np.full(
            (height, width), Back.GREEN + " " + Back.RESET, dtype="object"
        )
        self.height = height
        self.width = width
        self.window_should_close = False

    def render(self):
        out = ""
        for row in self.frame:
            for col in row:
                out += col
            out += "\n"
        sys.stdout.write(out)

    def add_object(self, object: GameObject):
        for i in range(object.size[0]):
            for j in range(object.size[1]):
                self.frame[object.position[0] + i][
                    object.position[1] + j
                ] = object.object[i][j]

    def clear(self):
        sp.call("clear", shell=True)

    def reset(self):
        self.frame = np.full(
            (self.height, self.width), Back.GREEN + " " + Back.RESET, dtype="object"
        )
