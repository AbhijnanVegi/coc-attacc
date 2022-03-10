import time
import numpy as np
from colorama import init, Fore, Back, Style

from game.input import Get,input_to
from game.scene import Scene
from game.game_object import GameObject
from game.building import TownHall, Wall, Hut, Cannon
from game.spawner import Spawner

class Game:
    def __init__(self):
        self.scene = Scene(120,30)
        self.get = Get()
        self.frame_rate = 1/60
        self.last_frame_time = 0
        self.buildings = []
        self.init()
        self.effects = []

    def init(self):
        self.buildings.append(TownHall(self, (5,50)))
        self.buildings.append(Spawner(self, (10,100)))
        self.buildings.append(Wall(self, (10,10)))
        self.buildings.append(Wall(self, (10,11)))
        self.buildings.append(Wall(self, (11,11)))
        self.buildings.append(Hut(self, (10,20)))
        self.buildings.append(Cannon(self, (10,30)))
        ...


    def update(self):
        for obj in self.buildings:
            obj.update()

    def process_input(self):
        i = input_to(self.get)
        if (i == 'q'):
            self.scene.window_should_close = True

    def run(self):
        while not self.scene.window_should_close:
            
            i = input_to(self.get)
            if (i == 'q'):
                self.scene.window_should_close = True

            while not (time.time() - self.last_frame_time) > self.frame_rate:
                pass

            self.process_input()
            self.scene.reset()
            self.update()
            self.scene.clear()
            self.scene.render()
            self.last_frame_time = time.time()

            
    
    def test(self):
        self.update()
        self.scene.render()