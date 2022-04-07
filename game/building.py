import numpy as np
from colorama import Fore, Back
import sys
import time

from game.colour_object import ColourObject
from game.config import (
    CNN_RANGE,
    CNN_RATE,
    TH_HP,
    WALL_HP,
    HUT_HP,
    CNN_HP,
    CNN_DMG,
    CNN_RANGE,
)
from game.utils import get_nearest_object, get_distance


class TownHall(ColourObject):
    def __init__(self, game, position: tuple):
        obj = np.full(
            (3, 4),
            Back.LIGHTBLACK_EX + "$" + Fore.RESET + Back.RESET,
            dtype="object",
        )
        super().__init__(game, position, obj, TH_HP)


class Wall(ColourObject):
    def __init__(self, game, position: tuple):
        obj = np.array(
            [[Back.LIGHTBLACK_EX + "*" + Fore.RESET + Back.RESET]], dtype="object"
        )
        super().__init__(game, position, obj, WALL_HP)


class Hut(ColourObject):
    def __init__(self, game, position: tuple):
        obj = np.full(
            (2, 3),
            Back.LIGHTBLACK_EX + "■" + Fore.RESET + Back.RESET,
            dtype="object",
        )
        super().__init__(game, position, obj, HUT_HP)


class Cannon(ColourObject):
    def __init__(self, game, position: tuple):
        obj = np.full(
            (2, 2),
            Back.LIGHTBLACK_EX + "●" + Fore.RESET + Back.RESET,
            dtype="object",
        )
        super().__init__(game, position, obj, CNN_HP)

        self.last_shot = 0
        self.range = CNN_RANGE
        self.damage = CNN_DMG
        self.rate = CNN_RATE

    def attack(self):
        if (time.time() - self.last_shot) < self.rate:
            return False
        nearest = get_nearest_object(
            self.game.units + [self.game.king],
            (self.position[0] + self.size[0] / 2, self.position[1] + self.size[1] / 2),
        )
        if not nearest:
            return False
        if (
            get_distance(
                (
                    self.position[0] + self.size[0] / 2,
                    self.position[1] + self.size[1] / 2,
                ),
                nearest.position,
            )
            < self.range
        ):
            nearest.health -= self.damage
            self.last_shot = time.time()
            return True
        return False

    def update(self):
        if self.attack():
            return super().update(colour=Fore.YELLOW)
        super().update()
