import pyxel
import Common

class Enemy:
    def __init__(self, x, y, w=8, h=8):
        self.x = x
        self.y = y
        self.w = 8  # Sprite Width
        self.h = 8  # Sprite Height

        self.col_x = 1 #Collision Box
        self.col_y = 1
        self.col_w = 6
        self.col_h = 6

        self.active = True



    def update(self):

        #self.y += 1  # 下方向に移動

        pass

    def draw(self):
        pyxel.blt(self.x, self.y, Common.TILE_BANK0, 
                  Common.SprList["ENEMY01_0"].x, Common.SprList["ENEMY01_0"].y,
                  self.w, self.h, pyxel.COLOR_BLACK)


        # Collision Box
        pyxel.rectb(self.x + self.col_x, self.y + self.col_y, self.col_w, self.col_h, pyxel.COLOR_RED)
