import pyxel
import Common
from ExplodeManager import ExpType

ANIM_FRAME = 10

class Enemy:
    def __init__(self, x, y, w=8, h=8, life=1, score=10, sprite_num=1):
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

        # Enemy sprite id (1-5)
        self.sprite_num = sprite_num

        self.active = True

        # Movement parameters are handled globally

    def update(self):

        if Common.StopTimer > 0:
            return

        # Individual enemies no longer handle movement here.
        # Movement is controlled at the formation level.

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
        AnimFrame = 10  #アニメーションの速度を変更できるよ
        anim_pat = pyxel.frame_count // AnimFrame % 4  # 0～3でぐるぐる（アニメ切り替え）

        # get sprite coordinates from Common by enemy number
        sprite_idx = Common.get_enemy_sprite(self.sprite_num, anim_pat)

        pyxel.blt(
            self.x,
            self.y,
            Common.TILE_BANK0,
            sprite_idx.x,
            sprite_idx.y,
            self.w,
            self.h,
            pyxel.COLOR_BLACK,
        )

        pyxel.pal()

        # Collision Box
        if Common.DEBUG:
            pyxel.rectb(self.x + self.col_x, self.y + self.col_y, self.col_w, self.col_h, pyxel.COLOR_RED)
