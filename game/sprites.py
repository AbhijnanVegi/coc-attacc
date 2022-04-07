import time
from colorama import Fore, Back
import numpy as np
import sys
from game.building import Cannon

from game.game_object import GameObject
from game.colour_object import ColourObject
from game.utils import (
    check_collision,
    get_nearest_object,
    get_distance,
    get_nearest_pos,
    check_inside,
)

from game.config import *


class Attacker(ColourObject):
    def __init__(
        self,
        game,
        position: tuple,
        object: np.ndarray,
        health: int,
        damage: int,
        rate: int,
        speed: int,
        range: int,
        aerial: bool = False,
    ):
        super().__init__(game, position, object, health)
        self.damage = damage
        self.rate = rate
        self.speed = speed
        self.range = range
        self.last_attack = time.time()
        self.last_move = time.time()
        self.aerial = aerial
        self.last_pos = (0, 0)

    def update(self):
        self.health *= self.game.effects["heal"]
        super().update()

    def _attack(self, object):
        if (time.time() - self.last_attack) > self.rate:
            self.last_attack = time.time()
            object.health -= self.damage * self.game.effects["damage"]
        ...

    def _move(self):
        ...

    def _in_range(self, object):
        if get_distance(self.position, object) <= self.range:
            return True
        return False

    def _undo(self):
        self.position = self.last_pos


class AutoAttacker(Attacker):
    def update(self):
        self.last_pos = self.position
        nearest = get_nearest_object(self._interests(), self.position)
        if not object:
            return super().update()
        nearest_cell = get_nearest_pos(nearest, self.position)
        if not nearest_cell:
            return super().update()
        if nearest is not None:
            ncell = get_nearest_pos(nearest, self.position)
            if not self._in_range(ncell):
                pos = self._move(nearest_cell)
                if not self.aerial:
                    for wall in self.game.walls:
                        if pos == wall.position:
                            self._undo()
                            self._attack(wall)
                            break
            else:
                self._attack(nearest)

        super().update()

    def _move(self, position: tuple):
        if (time.time() - self.last_move) < self.speed * self.game.effects["speed"]:
            return self.position
        self.last_move = time.time()
        new_pos_X, new_pos_Y = self.position
        if np.sign(position[0] - self.position[0]):
            new_pos_X = self.position[0] + np.sign(position[0] - self.position[0])
        else:
            new_pos_Y = self.position[1] + np.sign(position[1] - self.position[1])
        self.position = (new_pos_X, new_pos_Y)
        return self.position

    def _interests(self):
        ...


class Barbarian(AutoAttacker):
    def __init__(self, game, position: tuple):
        obj = np.array([[Back.YELLOW + "^" + Fore.RESET + Back.RESET]], dtype="object")
        super().__init__(
            game, position, obj, BARB_HP, BARB_DAMAGE, BARB_RATE, BARB_SPEED, BARB_RANGE
        )

    def _interests(self):
        return self.game.buildings


class Archer(AutoAttacker):
    def __init__(self, game, position: tuple):
        obj = np.array([[Back.MAGENTA + "^" + Fore.RESET + Back.RESET]], dtype="object")
        super().__init__(
            game, position, obj, ARCH_HP, ARCH_DAMAGE, ARCH_RATE, ARCH_SPEED, ARCH_RANGE
        )

    def _interests(self):
        return self.game.buildings


class Balloon(AutoAttacker):
    def __init__(self, game, position: tuple):
        obj = np.array([[Back.BLACK + "*" + Fore.RESET + Back.RESET]], dtype="object")
        super().__init__(
            game,
            position,
            obj,
            BAL_HP,
            BAL_DAMAGE,
            BAL_RATE,
            BAL_SPEED,
            BAL_RANGE,
            aerial=True,
        )

    def _interests(self):
        defenses = [
            building for building in self.game.buildings if isinstance(building, Cannon)
        ]
        return defenses if defenses else self.game.buildings


class ControlAttacker(Attacker):
    def handle_inp(self, key):
        if key in ["w", "a", "s", "d"]:
            self._move(key)
        elif key == " ":
            self._attack()

    def _attack(self):
        ...

    def _move(self, key):
        if (time.time() - self.last_move) < self.speed * self.game.effects["speed"]:
            return

        if key == "w":
            if self.position[0] > 0:
                self.position = (self.position[0] - 1, self.position[1])
                for building in self.game.buildings + self.game.walls:
                    if check_inside(self, building):
                        self.position = (self.position[0] + 1, self.position[1])
        elif key == "s":
            if self.position[0] < self.game.scene.height - 1:
                self.position = (self.position[0] + 1, self.position[1])
                for building in self.game.buildings + self.game.walls:
                    if check_inside(self, building):
                        self.position = (self.position[0] - 1, self.position[1])
        elif key == "a":
            if self.position[1] > 0:
                self.position = (self.position[0], self.position[1] - 1)
                for building in self.game.buildings + self.game.walls:
                    if check_inside(self, building):
                        self.position = (self.position[0], self.position[1] + 1)
        elif key == "d":
            if self.position[1] < self.game.scene.width - 1:
                self.position = (self.position[0], self.position[1] + 1)
                for building in self.game.buildings + self.game.walls:
                    if check_inside(self, building):
                        self.position = (self.position[0], self.position[1] - 1)


class King(ControlAttacker):
    def __init__(self, game, position):
        obj = np.array(
            [
                [
                    Back.YELLOW + "/" + Fore.RESET + Back.RESET,
                    Back.YELLOW + "\\" + Fore.RESET + Back.RESET,
                ],
                [
                    Back.YELLOW + "\\" + Fore.RESET + Back.RESET,
                    Back.YELLOW + "/" + Fore.RESET + Back.RESET,
                ],
            ],
            dtype="object",
        )
        super().__init__(
            game, position, obj, KING_HP, KING_DAMAGE, KING_RATE, KING_SPEED, KING_RANGE
        )

    def _attack(self):
        if (time.time() - self.last_attack) > self.rate:
            self.last_attack = time.time()
            for building in self.game.buildings + self.game.walls:
                nearest = get_nearest_pos(building, self.position)
                if (
                    get_distance(
                        (
                            self.position[0] + self.size[0] / 2,
                            self.position[1] + self.size[1] / 2,
                        ),
                        nearest,
                    )
                    < self.range
                ):
                    building.health -= self.damage * self.game.effects["damage"]
        ...


class Queen(ControlAttacker):
    def __init__(self, game, position):
        obj = np.array(
            [
                [
                    Back.MAGENTA + "/" + Fore.RESET + Back.RESET,
                    Back.MAGENTA + "\\" + Fore.RESET + Back.RESET,
                ],
                [
                    Back.MAGENTA + "\\" + Fore.RESET + Back.RESET,
                    Back.MAGENTA + "/" + Fore.RESET + Back.RESET,
                ],
            ],
            dtype="object",
        )
        super().__init__(
            game,
            position,
            obj,
            QUEEN_HP,
            QUEEN_DAMAGE,
            QUEEN_RATE,
            QUEEN_SPEED,
            QUEEN_RANGE,
        )
        self.aoe = QUEEN_AOE
        self.last_direction = (0, 0)

    def _attack(self):
        if time.time() - self.last_attack < self.rate:
            return

        center = (
            self.position[0] + self.size[0] / 2 + self.range * self.last_direction[0],
            self.position[1] + self.size[1] / 2 + self.range * self.last_direction[1],
        )

        for building in self.game.buildings + self.game.walls:
            nearest = get_nearest_pos(building, center)
            if get_distance(center, nearest) < self.range:
                building.health -= self.damage * self.game.effects["damage"]

    def handle_inp(self, key):
        if key == "w":
            self.last_direction = (-1, 0)
        elif key == "s":
            self.last_direction = (1, 0)
        elif key == "a":
            self.last_direction = (0, -1)
        elif key == "d":
            self.last_direction = (0, 1)
        super().handle_inp(key)
