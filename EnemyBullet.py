import pyxel
import Common

class EnemyBullet:
    def __init__(self, x, y, w=8, h=8, speed=2):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.col_x = 2  # Collision Box
        self.col_y = 2
        self.col_w = 4
        self.col_h = 4

        self.speed = speed
        self.active = True

    def update(self):
        self.y += self.speed
        if self.y > Common.WIN_HEIGHT:  # 画面外に出たら消す
            self.active = False

    def draw(self):
        pyxel.blt(self.x, self.y, Common.TILE_BANK0,
                Common.SprList["ENEMY_BULLET"].x, Common.SprList["ENEMY_BULLET"].y, 
                self.w, self.h, pyxel.COLOR_BLACK)
   
        # Collision Box
        if Common.DEBUG:
            pyxel.rectb(self.x + self.col_x, self.y + self.col_y, 
                       self.col_w, self.col_h, pyxel.COLOR_RED) 