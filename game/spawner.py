import numpy as np
from colorama import Fore, Back

from game.game_object import GameObject
from game.sprites import Barbarian

class Spawner(GameObject):
    def __init__(self, game, position: tuple):
        obj = np.array([[Back.WHITE + Fore.RED + '✕' + Fore.RESET + Back.RESET]])
        super().__init__(game, position, obj)
        self.game = game

    def spawn_barb(self):
        self.game.units.append(Barbarian(self.game, self.position))

