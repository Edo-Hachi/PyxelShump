import pyxel
import Common
import math

from Bullet import Bullet

ExtNames = ["EXT01", "EXT02", "EXT03", "EXT04"]
ExtMax = len(ExtNames)

SHOTTIMER = 8  # 弾の発射間隔

MuzlNames = ["MUZL01", "MUZL02", "MUZL03"] #0-2
MuzlStarIndex = 2

EXPLODE_TIMER=180

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 8
        self.height = 8

        self.col_x = 2  # Collision X
        self.col_y = 2  # Collision Y
        self.col_w = 4  # Collision Width
        self.col_h = 4

        self.speed = 1
        self.col_active = True
        self.ShotTimer = SHOTTIMER

        self.ExplodeCoolTimer = -1 #EXPLODE_TIMER
        self.NowExploding = False

        self.SprName = "TOP"    #Drawing Sprite Name

        self.ExtIndex = 0
        self.ExtSpr = "EXT01"  # Exhaust Sprite Name

        self.MuzlFlash = 0  # Muzzle Flash List



    def update(self):
        #Exhaust Animation --------
        self.ExtSpr = ExtNames[self.ExtIndex]
        
        self.ExtIndex += 1
        if self.ExtIndex >= ExtMax:
            self.ExtIndex = 0

        #Movement -----------
        self.SprName = "TOP"
        dx = 0  #direction
        dy = 0

        if pyxel.btn(pyxel.KEY_LEFT):
            dx -= 1
            self.SprName = "LEFT"

        if pyxel.btn(pyxel.KEY_RIGHT):
            dx += 1
            self.SprName = "RIGHT"

        if pyxel.btn(pyxel.KEY_UP):
            dy -= 1
        if pyxel.btn(pyxel.KEY_DOWN):
            dy += 1 

        # Normalize(斜め移動ならスピード調整（0.6倍）)
        if dx != 0 and dy != 0:
            dx *= 0.6
            dy *= 0.6

        self.x += dx * self.speed
        self.y += dy * self.speed

        # 画面端での境界チェック
        self.x = max(0, min(self.x, Common.WIN_WIDTH - self.width))
        self.y = max(0, min(self.y, Common.WIN_HEIGHT - (self.height+8)))
        
        #弾の発射
        if pyxel.btn(pyxel.KEY_SPACE):
            if(self.ShotTimer <= 0):
                pyxel.play(0, 0)  # 効果音再生
                Common.player_bullet_list.append(Bullet(self.x-4, self.y-4, 8, 8)) # 弾の情報をリストに追加
                Common.player_bullet_list.append(Bullet(self.x+4, self.y-4, 8, 8)) # 弾の情報をリストに追加
                self.ShotTimer = SHOTTIMER  # 再発射までの時間をリセット

                self.MuzlFlash = MuzlStarIndex  # Muzzle Flash Animate Start

        
        self.ShotTimer -= 1  # 発射間隔のカウントダウン
            
        # 弾の更新と削除
#        for _bullet in Common.player_bullet_list:
#            _bullet.update()
#        Common.player_bullet_list = [b for b in Common.player_bullet_list if b.active]

        #プレイヤーと敵との当たり判定(ExplodeCoolTimerがプラス値ならクールタイム中)
        if self.ExplodeCoolTimer < 0:
            for _enemy in Common.enemy_list:
                if self.col_active and _enemy.active:

                    if Common.check_collision(self.x + self.col_x, self.y + self.col_y, self.col_w, self.col_h,
                                        _enemy.x + _enemy.col_x, _enemy.y + _enemy.col_y, _enemy.col_w, _enemy.col_h):

                        #爆発エフェクト   
                        Common.explode_manager.SpawnExplode_Circle(self.x + 4, self.y + 4, 20)
                        #一度接触すると3秒クールタイム
                        self.ExplodeCoolTimer = EXPLODE_TIMER
                        self.NowExploding = True

                    #Common.GameState = Common.STATE_GAMEOVER
        else:
            self.NowExploding = False
            #点滅処理とか
            pass
            self.ExplodeCoolTimer-=1

    
    def draw(self):

        if self.ExplodeCoolTimer < 0:
            #print("Ship Active")
            pyxel.blt(self.x, self.y, Common.TILE_BANK0,
                Common.SprList[self.SprName].x, Common.SprList[self.SprName].y, self.width, self.height, pyxel.COLOR_BLACK)
        else:
            #print("Cool Time")
            if math.sin(Common.GameTimer/3) < 0:
                for n in range(1, 15):
                    pyxel.pal(n,pyxel.COLOR_YELLOW)

            pyxel.blt(self.x, self.y, Common.TILE_BANK0,
                Common.SprList[self.SprName].x, Common.SprList[self.SprName].y, self.width, self.height, pyxel.COLOR_BLACK)

        


        pyxel.blt(self.x, self.y, Common.TILE_BANK0,
            Common.SprList[self.SprName].x, Common.SprList[self.SprName].y, self.width, self.height, pyxel.COLOR_BLACK)

        #Exhaust
        pyxel.blt(self.x, self.y+8, Common.TILE_BANK0,
            Common.SprList[self.ExtSpr].x, Common.SprList[self.ExtSpr].y, self.width, self.height, pyxel.COLOR_BLACK)

        #Muzzle Flash
        if self.MuzlFlash >= 0:
            pyxel.blt(self.x-4, self.y-6, Common.TILE_BANK0,
                      Common.SprList[MuzlNames[self.MuzlFlash]].x, Common.SprList[MuzlNames[self.MuzlFlash]].y, 8, 8, pyxel.COLOR_BLACK)
            pyxel.blt(self.x+4, self.y-6, Common.TILE_BANK0,
                      Common.SprList[MuzlNames[self.MuzlFlash]].x, Common.SprList[MuzlNames[self.MuzlFlash]].y, 8, 8, pyxel.COLOR_BLACK)

        self.MuzlFlash -= 1
        
        #弾描画
        for _bullet in Common.player_bullet_list:
            _bullet.draw()
       

        # Collision Box 
        if Common.DEBUG:
            pyxel.rectb(self.x + self.col_x, self.y + self.col_y, self.col_w, self.col_h, pyxel.COLOR_GREEN)
