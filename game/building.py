import numpy as np
from colorama import Fore, Back
import sys
import time

from game.colour_object import ColourObject
from game.config import *
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


class Defense(ColourObject):
    def __init__(
        self,
        game,
        position: tuple,
        obj: np.ndarray,
        hp: int,
        damage: int,
        rate: int,
        range: int,
    ):
        super().__init__(game, position, obj, hp)
        self.damage = damage
        self.rate = rate
        self.range = range
        self.last_shot = time.time()

    def _attack(self):
        ...

    def update(self):
        if self._attack():
            return super().update(colour=Fore.YELLOW)
        super().update()


class Cannon(Defense):
    def __init__(self, game, position: tuple):
        obj = np.full(
            (2, 2),
            Back.LIGHTBLACK_EX + "●" + Fore.RESET + Back.RESET,
            dtype="object",
        )
        super().__init__(game, position, obj, CNN_HP, CNN_DMG, CNN_RATE, CNN_RANGE)

    def _attack(self):
        if (time.time() - self.last_shot) < self.rate:
            return False
        nearest = get_nearest_object(
            self._interests(),
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

    def _interests(self):
        return [unit for unit in self.game.units if not unit.aerial] + [self.game.king]


class WizardTower(Defense):
    def __init__(self, game, position):
        obj = np.full(
            (3, 2), Back.LIGHTBLACK_EX + "%" + Fore.RESET + Back.RESET, dtype="object"
        )
        super().__init__(game, position, obj, WT_HP, WT_DMG, WT_RATE, WT_RANGE)

    def _attack(self):
        if (time.time() - self.last_shot) < self.rate:
            return False
        nearest = get_nearest_object(
            self._interests(),
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
            for unit in self._interests():
                if (abs(unit.position[0] - nearest.position[0]) <= 1) and (
                    abs(unit.position[1] - nearest.position[1]) <= 1
                ):
                    unit.health -= self.damage
            self.last_shot = time.time()
            return True
        return False

    def _interests(self):
        return self.game.units + [self.game.king]
