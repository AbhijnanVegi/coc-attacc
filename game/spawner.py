import numpy as np
from colorama import Fore, Back
import sys

from game.game_object import GameObject
from game.sprites import Archer, Balloon, Barbarian

BARB = 0
ARCHER = 1
LOON = 2

class Spawner(GameObject):
    def __init__(self, game, position: tuple):
        obj = np.array([[Back.WHITE + Fore.RED + "✕" + Fore.RESET + Back.RESET]])
        super().__init__(game, position, obj)
        self.game = game

    def spawn(self, troop: int):
        if (troop == BARB):
            self.game.units.append(Barbarian(self.game, self.position))
        elif (troop == ARCHER):
            self.game.units.append(Archer(self.game, self.position))
        elif (troop == LOON):
            self.game.units.append(Balloon(self.game, self.position))
