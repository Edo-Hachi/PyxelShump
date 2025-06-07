import pyxel
import Common
from ExplodeManager import ExpType

ANIM_FRAME = 10

class Enemy:
    def __init__(self, x, y, w=8, h=8, life = 1, score=10):
        self.x = x
        self.y = y
        self.w = w  # Sprite Width
        self.h = h  # Sprite Height

        self.col_x = 1 #Collision Box
        self.col_y = 1
        self.col_w = 6
        self.col_h = 6

        self.Life = life
        self.Score = score

        self.flash = 0

        self.active = True

    def update(self):
        
        if Common.StopTimer > 0:
            return  

    def on_hit(self, bullet):
        # 弾を消す
        bullet.active = False
        self.Life -= 1
        
        if self.Life <= 0:
            self.active = False  # エネミーを非アクティブに
            Common.Score += self.Score  # スコア加算
            pyxel.play(0, 1)  # 効果音再生
            Common.explode_manager.spawn_explosion(self.x + 4, self.y + 4, 20, ExpType.RECT)
            #Common.explode_manager.spawn_explosion(self.x + 4, self.y + 4, 20, ExpType.CIRCLE)
        else:
            self.flash = 6  # 点滅処理
            Common.explode_manager.spawn_explosion(self.x + 4, self.y + 8, 5, ExpType.DOT_REFRECT)

            pyxel.play(0, 2)  # 効果音再生


    def draw(self):
        if self.flash > 0:
            # Flash
            for i in range(1, 15):
                pyxel.pal(i, pyxel.COLOR_WHITE)

        self.flash -= 1

        #anim_pat = 0 ~ 3
        ANIM_FRAME = 10
        anim_pat = pyxel.frame_count // ANIM_FRAME % 4  # 0～3でぐるぐる（アニメ切り替え）

        sprite_key = f"ENEMY01_{anim_pat}"  # → "ENEMY01_0"～"ENEMY01_3"
        
        pyxel.blt(self.x, self.y, Common.TILE_BANK0, 
                  Common.SprList[sprite_key].x, Common.SprList[sprite_key].y,
                  #Common.SprList["ENEMY01_0"].x, Common.SprList["ENEMY01_0"].y,
                  #Common.SprList["ENEMY05_0"].x, Common.SprList["ENEMY05_0"].y,
                  self.w, self.h, pyxel.COLOR_BLACK)

        pyxel.pal()

        # Collision Box
        if Common.DEBUG:
            pyxel.rectb(self.x + self.col_x, self.y + self.col_y, self.col_w, self.col_h, pyxel.COLOR_RED)
