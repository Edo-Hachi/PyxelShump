import pyxel
import Common

#BLT_SPEED = 8

class Bullet:
    def __init__(self, x, y, w, h, speed=3):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.col_x = 2 #Collision Box
        self.col_y = 2
        self.col_w = 4
        self.col_h = 4
        self.active = True

        self.speed = speed

        self.active = True  # アクティブフラグ


    def update(self):
        self.y -= self.speed
        if self.y < -16: # 画面外に出たら消す
            self.active = False #実際のガベコレはplayer.pyでやってます

        for _enemy in Common.enemy_list:
            if _enemy.active:
                if Common.check_collision(self.x + self.col_x, self.y + self.col_y, self.col_w, self.col_h,
                                        _enemy.x + _enemy.col_x, _enemy.y + _enemy.col_y, _enemy.col_w, _enemy.col_h):


#                if Common.check_collision(self.player.x + self.player.col_x, self.player.y + self.player.col_y, self.player.col_w, self.player.col_h,
 #                                      _enemy.x + _enemy.col_x, _enemy.y + _enemy.col_y, _enemy.col_w, _enemy.col_h):

                    self.active = False #実際のガベコレはplayer.pyでやってます

                    print("Hit!")

    def draw(self):
        pyxel.blt(self.x, self.y, Common.TILE_BANK0,
                Common.SprList["BULLET01"].x, Common.SprList["BULLET01"].y, 8, 8, pyxel.COLOR_BLACK)

#        pyxel.blt(self.x, self.y, Common.TILE_BANK0,
#                Common.SprList["BULLET02"].x, Common.SprList["BULLET02"].y, 8, 8, pyxel.COLOR_BLACK)
   
       # Collision Box
        pyxel.rectb(self.x + self.col_x, self.y + self.col_y, self.col_w, self.col_h, pyxel.COLOR_RED)

