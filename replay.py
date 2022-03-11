import time
import sys
import subprocess as sp
import pickle

class Replay:
    def __init__(self, frames):
        self.frame = None
        self.frames = frames
        self.frame_rate = 1/60
        self.last_frame_time = time.time()
        self.frame_count = 0

    def run(self):
        while self.frame_count < len(self.frames):
            while not (time.time() - self.last_frame_time) > self.frame_rate:
                pass

            self.frame = self.frames[self.frame_count]
            sp.call("clear", shell=True)
            self.render()
            self.last_frame_time = time.time()
            self.frame_count += 1


    def render(self):
        out = ""
        for row in self.frame:
            for col in row:
                out += col
            out += "\n"
        sys.stdout.write(out)

if __name__=='__main__':
    rep = input("Enter name of replay: ")
    with open('replays/' + rep + '.replay', "rb") as f:
        replay = Replay(pickle.load(f))
    replay.run()

