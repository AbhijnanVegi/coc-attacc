import time
from colorama import Fore, Back
import numpy as np
import sys

from game.game_object import GameObject
from game.colour_object import ColourObject
from game.utils import (
    check_collision,
    get_nearest_object,
    get_distance,
    get_nearest_pos,
    check_inside,
)

from game.config import (
    BARB_HP,
    BARB_DAMAGE,
    BARB_RATE,
    BARB_SPEED,
    BARB_RANGE,
    KING_HP,
    KING_DAMAGE,
    KING_RANGE,
    KING_RATE,
    KING_SPEED,
)


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
        self.last_pos = (0,0)

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

    def undo(self):
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
            print(nearest.position,self.position,nearest.size, ncell, file=sys.stderr)
            if not self._in_range(ncell):
                wall = get_nearest_object(self.game.walls, self.position)
                if check_collision(self, wall) and not self.aerial:
                    self._attack(wall)
                else:
                    self._move(nearest_cell)
            else:
                self._attack(nearest)
        super().update()

    def _move(self, position: tuple):
        if (time.time() - self.last_move) < self.speed * self.game.effects["speed"]:
            return
        self.last_move = time.time()
        new_pos_X, new_pos_Y = self.position
        if (np.sign(position[0] - self.position[0])):
            new_pos_X = self.position[0] + np.sign(position[0] - self.position[0])
        else:
            new_pos_Y = self.position[1] + np.sign(position[1] - self.position[1])
        self.position = (new_pos_X, new_pos_Y)

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


# class Archer(AutoAttacker):
#     def __init__(self,game, position:tuple):
#         obj = np.array([[Back.MAGENTA + "^" + Fore.RESET + Back.RESET]], dtype="object")
#         super().__init__(
#             game, position, obj,
#         )


class King(Attacker):
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

    def handle_inp(self, key):
        if key in ["w", "a", "s", "d"]:
            self._move(key)
        elif key == " ":
            self._attack()

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
