import pyxel
import random
from Explode import Explode
import Common

class ExplodeManager:
    def __init__(self):
        self.explosions = []

    def spawn_explosion(self, x, y, count=20):
        for _ in range(count):
            self.explosions.append(Explode(x, y))

    def update(self):
        for e in self.explosions:
            e.update()
        self.explosions = [e for e in self.explosions if e.is_alive]

    def draw(self):
        for e in self.explosions:
            e.draw()
