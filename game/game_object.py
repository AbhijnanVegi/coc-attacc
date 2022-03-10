from pandas import array
import numpy as np

class GameObject:
    def __init__(self,game,position:tuple, object:np.ndarray):
        self.position = position
        self.object = object
        self.size = object.shape
        self.game = game
        
    def update(self):
        self.game.scene.add_object(self)