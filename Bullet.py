import pyxel
import Common

BLT_SPEED = 8

class Bullet:
    def __init__(self, x, y, speed=5):
        self.x = x
        self.y = y
        #self.speed = 4
        self.active = True  # 消すフラグ

        pyxel.play(0, 0)  # 効果音再生

    def update(self):
        self.y -= BLT_SPEED
        if self.y < -8: # 画面外に出たら消す
            self.active = False

    def draw(self):
        #pyxel.circ(self.x, self.y, 1, 7)  # 小さい白い弾
        pyxel.blt(self.x, self.y, Common.TILE_BANK0,
            Common.SprList["BULLET"].x, Common.SprList["BULLET"].y,
            8, 8, pyxel.COLOR_BLACK)
        

