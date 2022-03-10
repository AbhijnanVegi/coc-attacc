import numpy as np
from colorama import Fore, Back

from game.game_object import GameObject
from game.config import CNN_RANGE, TH_HP, WALL_HP, HUT_HP, CNN_HP, CNN_DMG, CNN_RANGE

class ColourObject(GameObject):
    def __init__(self, game, position: tuple, object: np.ndarray, health: int):
        super().__init__(game, position, object)
        self.colour = Fore.GREEN
        self.max_health = health
        self.health = health
        self.template = object

    def update(self):
        if self.health <= 0:
            self.game.remove_object(self)
        if self.health > self.max_health:
            self.health = self.max_health
        if self.health < 0.5 * self.max_health:
            self.colour = Fore.YELLOW
        if self.health < 0.2 * self.max_health:
            self.colour = Fore.RED

        self.update_object()
        super().update()

    def update_object(self):
        size = self.object.shape
        for i in range(size[0]):
            for j in range(size[1]):
                self.object[i][j] = self.colour + self.template[i][j]


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
        obj = np.array([[Back.LIGHTBLACK_EX + '*' + Fore.RESET + Back.RESET]], dtype="object")
        super().__init__(game, position, obj, WALL_HP)

class Hut(ColourObject):
    def __init__(self, game, position: tuple):
        obj = np.full(
            (2,3),
            Back.LIGHTBLACK_EX + '■' + Fore.RESET + Back.RESET,
            dtype="object",
        )
        super().__init__(game, position, obj, HUT_HP)

class Cannon(ColourObject):
    def __init__(self, game, position: tuple):
        obj = np.full(
            (2,2),
            Back.LIGHTBLACK_EX + '●' + Fore.RESET + Back.RESET,
            dtype="object",
        )
        super().__init__(game, position, obj, CNN_HP)

        self.last_shot = 0
        self.range = CNN_RANGE
        self.damage = CNN_DMG



    
        

