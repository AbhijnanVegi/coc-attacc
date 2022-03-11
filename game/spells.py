import time
import sys

class Spell:
    def __init__(self,game, duration):
        self.duration = duration
        self.start_time = None
        self.effects = {}
        self.game = game

    def use(self):
        if not self.start_time:
            self.start_time = time.time()

    def update(self):
        if self.start_time is None:
            return
        if time.time() - self.start_time < self.duration:
            for key in self.effects.keys():
                self.game.effects[key] = self.effects[key]

class Rage(Spell):
    def __init__(self, game, duration):
        super().__init__(game, duration)
        self.effects = {
            "damage": 2,
            "speed": 0.5,
        }


class Heal(Spell):
    def __init__(self, game, duration):
        super().__init__(game, duration)
        self.effects = {
            "heal": 1.5,
        }



