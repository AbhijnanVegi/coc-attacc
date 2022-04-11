import time
import numpy as np
from colorama import init, Fore, Back, Style
import sys
import pickle
import json
import math

from game.colour_object import ColourObject
from game.input import Get, input_to
from game.scene import Scene
from game.game_object import GameObject
from game.building import TownHall, Wall, Hut, Cannon, WizardTower
from game.spawner import Spawner
from game.sprites import Barbarian, King, Queen
from game.spells import Rage, Heal




class Game:
    def __init__(self):
        self.scene = Scene(120, 30)
        self.get = Get()
        self.frame_rate = 1 / 60
        self.last_frame_time = time.time()

        self.buildings = []
        self.walls = []
        self.spawners = []

        self.max_units = [10, 5, 3]
        self.units = []
        self.king = None
        self.champ_type = None

        self.spells = []
        self.effects = {
            "speed": 1,
            "damage": 1,
            "rate": 1,
            "heal": 1,
        }

        self.frames = []

        self.current_level = None
        self.levels = []

        self.init()

    def init(self):

        lvl = input("Enter level to load: ")
        self.current_level = 0
        self.levels = self.load_levels(lvl)
        champ = input("[K]ing or [Q]ueen? ")
        if champ[0].lower() == "k":
            self.champ_type = King
        elif champ[0].lower() == "q":
            self.champ_type = Queen
        else:
            print("Invalid champion")
            sys.exit()
        self.load_level(self.current_level)

    def load_levels(self, lvl:str):
        with open('levels/' + lvl + '.json', 'r') as f:
            return json.load(f)

    def load_level(self, lvl:int):
        level = self.levels[lvl]
        self.units = []
        for building in level["buildings"]:
            if building["type"] == "th":
                self.buildings.append(
                    TownHall(self, (building["location"][0], building["location"][1]))
                )
            elif building["type"] == "hut":
                self.buildings.append(
                    Hut(self, (building["location"][0], building["location"][1]))
                )
            elif building["type"] == "cannon":
                self.buildings.append(
                    Cannon(
                        self, (building["location"][0], building["location"][1])
                    )
                )
            elif building["type"] == "wt":
                self.buildings.append(
                    WizardTower(
                        self, (building["location"][0], building["location"][1])
                    )
                )

        for wall in level["walls"]:
            for i in range(wall["length"]):
                self.walls.append(
                    Wall(
                        self,
                        (
                            wall["location"][0] + i * wall["direction"][0],
                            wall["location"][1] + i * wall["direction"][1],
                        ),
                    )
                )

        for spawner in level["spawners"]:
            self.spawners.append(Spawner(self, (spawner[0], spawner[1])))

        self.max_units = level["troops"]
        self.king = self.champ_type(self, (level["king"]["location"][0], level["king"]["location"][1]))

        

    def update(self):

        for obj in self.buildings:
            obj.update()
        for spawner in self.spawners:
            spawner.update()
        for wall in self.walls:
            wall.update()
        for unit in self.units:
            unit.update()
        if self.king:
            self.king.update()

    def process_input(self):
        i = input_to(self.get, timeout=0.05)
        if i == "q":
            self.scene.window_should_close = True

        if i in ["w", "a", "s", "d", " ", "e"]:
            if self.king:
                self.king.handle_inp(i)

        if i in [str(i) for i in range(1, 10)]:
            try:
                if self.max_units[int((int(i) - 1) / 3)]:
                    self.spawners[int(i) % 3].spawn(int((int(i) - 1) / 3))
                    self.max_units[int((int(i) - 1) / 3)] -= 1
            except Exception as e:
                print(e, file=sys.stderr)


    def show_hud(self):
        def format_hp(hp):
            count = math.ceil(hp / 25)
            return "█" * count + " " * (10 - count)

        print(Fore.YELLOW + "Troops: " + str(self.max_units) + Fore.RESET, end="  ")
        if self.king:
            print(
                "King Health: "
                + self.king.colour
                + format_hp(self.king.health)
                + Fore.RESET
            )
        else:
            print("King Health: " + Fore.RED + "DEAD" + Fore.RESET)
        print()

    def run(self):
        while not self.scene.window_should_close:

            while not (time.time() - self.last_frame_time) > self.frame_rate:
                pass
            self.effects_update()
            self.process_input()
            self.scene.reset()
            self.update()
            self.scene.clear()
            self.show_hud()
            self.scene.render()
            self.frames.append(self.scene.frame)
            end, win = self.check_game_end()
            if end:
                if self.end(win):
                    break
            self.last_frame_time = time.time()

    def test(self):
        self.update()
        self.scene.render()

    def remove_object(self, object: ColourObject):
        try:
            self.buildings.remove(object)
            return
        except:
            ...
        try:
            self.walls.remove(object)
            return
        except:
            ...
        try:
            self.units.remove(object)
            return
        except:
            ...
        if object == self.king:
            self.king = None

    def check_game_end(self) -> tuple:
        if self.buildings == []:
            return True, True
        elif self.max_units == [] and self.units == [] and not self.king:
            return True, False
        else:
            return False, None

    def end(self, win: bool):
        if win:
            self.current_level += 1
            print(self.current_level, len(self.levels), file=sys.stderr)
            if self.current_level == len(self.levels):
                print("You win!")
            else:
                self.load_level(self.current_level)
                return False
        else:
            print("Game Over!")
        sys.stdout.write("Enter name of replay: ")
        loc = input()
        with open("replays/" + loc + ".replay", "wb") as f:
            pickle.dump(self.frames, f)
        return True
        ...

    def effects_update(self):
        self.effects["speed"] = 1
        self.effects["damage"] = 1
        self.effects["rate"] = 1
        self.effects["heal"] = 1

        for spell in self.spells:
            spell.update()
