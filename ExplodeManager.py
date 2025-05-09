import pyxel
import random
from dataclasses import dataclass
import Common

class Explode:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = random.uniform(-1.5, 1.5)
        self.dy = random.uniform(-1.5, 1.5)
        self.life = random.randint(5, 10)
        self.col = random.randint(8, 15)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.life -= 1

    def draw(self):
        if self.life > 0:
            pyxel.pset(int(self.x), int(self.y), self.col)

    @property
    def is_alive(self):
        return self.life > 0


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
