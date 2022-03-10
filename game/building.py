import numpy as np
from colorama import Fore, Back

from game.colour_object import ColourObject
from game.config import CNN_RANGE, TH_HP, WALL_HP, HUT_HP, CNN_HP, CNN_DMG, CNN_RANGE

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



    
        

