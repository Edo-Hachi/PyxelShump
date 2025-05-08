import pyxel
import Common

class Enemy:
    def __init__(self, x, y, w=8, h=8):
        self.x = x
        self.y = y
        self.w = 8  # Sprite Width
        self.h = 8  # Sprite Height

        self.x1 = 0 #Collision Box
        self.y1 = 0
        self.x2 = 8
        self.y2 = 8
        self.active = True



    def update(self):
        #self.y += 1  # 下方向に移動
        pass

    def draw(self):
        pyxel.blt(self.x, self.y, Common.TILE_BANK0, 
                  Common.SprList["ENEMY01_0"].x, Common.SprList["ENEMY01_0"].y,
                  self.w, self.h, pyxel.COLOR_BLACK)


        # Collision Box
        pyxel.rectb(self.x + self.x1, self.y + self.y1, self.x2, self.y2, pyxel.COLOR_RED)

# def draw_enemy(self):
#     self.enemy_spr = (self.enemy_spr + 0.1) % 3.5
#     sprname = f"ENEMY01_{round(self.enemy_spr)}"

#     pyxel.blt(self.enemy_x, self.enemy_y, Common.TILE_BANK0,
#             Common.SprList[sprname].x, Common.SprList[sprname].y, 8, 8, pyxel.COLOR_BLACK)
    
#     self.enemy_y += 1
#     if self.enemy_y > Common.WIN_HEIGHT:
#         self.enemy_y = 0
#         self.enemy_x = random.randint(0, Common.WIN_WIDTH - 8)