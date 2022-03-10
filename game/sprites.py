from colorama import Fore, Back
import numpy as np

from game.game_object import GameObject

class Sprite(GameObject):
    def __init__(self, game, position: tuple, object: np.ndarray, health:int):
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

