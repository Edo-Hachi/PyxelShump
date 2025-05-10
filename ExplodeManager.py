import pyxel
import random
from dataclasses import dataclass
#from enum import Enum, auto


#MAX_EXPLOSIONS = 200

# class ParticleType(Enum):
#     PSET = auto()
#     RECT = auto()
#     CIRCLE = auto()


class Explode_RECT:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = random.randint(2, 6)
        self.h = random.randint(2, 6)   
        self.dx = random.uniform(-1.5, 1.5)
        self.dy = random.uniform(-1.5, 1.5)
        self.life = random.randint(3, 20)   #弾の寿命大きいと長く飛び散ります
        self.col = random.randint(8, 15)

    def update(self):
            self.x += self.dx
            self.y += self.dy

            self.w -= 0.05
            self.h -= 0.05  

            self.life -= 1

            #爆発パーティクルの速度減衰
            self.dx *= 0.90
            self.dy *= 0.90


    def draw(self):
        if self.life > 0:
                #pyxel.pset(int(self.x), int(self.y), self.col)
                _color = pyxel.COLOR_WHITE
                
                if 15 < self.life:
                    _color = pyxel.COLOR_WHITE
                elif 10 < self.life and self.life <= 14:
                    _color = pyxel.COLOR_ORANGE
                elif 6 < self.life and self.life <= 10:
                    _color = pyxel.COLOR_YELLOW
                elif 3 < self.life and self.life <= 5:
                    _color = pyxel.COLOR_BROWN
                elif 0 < self.life and self.life <= 3:
                    _color = pyxel.COLOR_GRAY


                pyxel.rect(int(self.x), int(self.y), self.w, self.h, _color)

    @property
    def is_alive(self):
        return self.life > 0


class Explode_DOT:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = random.uniform(-1.5, 1.5)
        self.dy = random.uniform(-1.5, 1.5)
        self.life = random.randint(5, 20)   #弾の寿命大きいと長く飛び散ります
        self.col = random.randint(8, 15)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.life -= 1

        #爆発パーティクルの速度減衰
        self.dx *= 0.90
        self.dy *= 0.90

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
        #for _ in range(count):
        for r in range(count):
            #self.explosions.append(Explode_DOT(x + 4, y + 4))   #8x8スプライトの中心あたりから発生
            self.explosions.append(Explode_RECT(x + 4, y + 4))   #8x8スプライトの中心あたりから発生

    def update(self):
        for exp in self.explosions:
            exp.update()
        self.explosions = [exp for exp in self.explosions if exp.is_alive]
        #self.explosions = self.explosions[-MAX_EXPLOSIONS:]

    def draw(self):
        for exp in self.explosions:
            exp.draw()
