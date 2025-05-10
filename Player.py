import pyxel
import Common

from Bullet import Bullet

ExtNames = ["EXT01", "EXT02", "EXT03", "EXT04"]
ExtMax = len(ExtNames)

SHOTTIMER = 7  # 弾の発射間隔

MuzlNames = ["MUZL01", "MUZL02", "MUZL03"]
#MuzlMax = len(ExtNames)
#MuzlList = []

class MuzzleFlash:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.life = 3  # Flash duration
        self.active = True
    
    def update(self):
        self.life -= 1
        if self.life <  0:
            self.active = False
    
    def draw(self):
        if self.active:
            pyxel.blt(self.x, self.y, Common.TILE_BANK0,
                      Common.SprList[MuzlNames[self.life]].x, Common.SprList[MuzlNames[self.life]].y, 8, 8, pyxel.COLOR_BLACK)



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

        self.SprName = "TOP"    #Drawing Sprite Name

        self.ExtIndex = 0
        self.ExtSpr = "EXT01"  # Exhaust Sprite Name

        self.MuzlList = []



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

                self.MuzlList.append(MuzzleFlash(self.x-4, self.y-6))  # Muzzle Flashを追加
                self.MuzlList.append(MuzzleFlash(self.x+4, self.y-6))  # Muzzle Flashを追加

        
        self.ShotTimer -= 1  # 発射間隔のカウントダウン
            
        # 弾の更新と削除
        for _bullet in Common.player_bullet_list:
            _bullet.update()
        Common.player_bullet_list = [b for b in Common.player_bullet_list if b.active]

        # Muzzle Flashの描画、削除
        for _muzzle in self.MuzlList:
            _muzzle.update()
        
        self.MuzlList = [m for m in self.MuzlList if m.active]


        # # 新しく空のリストを用意
        # new_bullet_list = []

        # # もともとの player_bullet_list を1つずつ確認
        # for b in Common.player_bullet_list:
        #     # b が active（有効）ならば新しいリストに追加
        #     if b.active:
        #         new_bullet_list.append(b)

        # # 最後に Common.player_bullet_list を更新する
        # Common.player_bullet_list = new_bullet_list

        #プレイヤーと敵との当たり判定
        for _enemy in Common.enemy_list:
            if self.col_active and _enemy.active:

                if Common.check_collision(self.x + self.col_x, self.y + self.col_y, self.col_w, self.col_h,
                                       _enemy.x + _enemy.col_x, _enemy.y + _enemy.col_y, _enemy.col_w, _enemy.col_h):

                    Common.GameState = Common.STATE_GAMEOVER

    
    def draw(self):

        #Player Ship
        pyxel.blt(self.x, self.y, Common.TILE_BANK0,
            Common.SprList[self.SprName].x, Common.SprList[self.SprName].y, self.width, self.height, pyxel.COLOR_BLACK)

        #Exhaust
        pyxel.blt(self.x, self.y+8, Common.TILE_BANK0,
            #Common.SprList[ExtNames[self.ExtIndex]].x, Common.SprList[ExtNames[self.ExtIndex]].y, self.width, self.height, pyxel.COLOR_BLACK)
            Common.SprList[self.ExtSpr].x, Common.SprList[self.ExtSpr].y, self.width, self.height, pyxel.COLOR_BLACK)


        #Muzzle Flash
        for _muzzle in self.MuzlList:
            _muzzle.draw()

        #弾描画
        for _bullet in Common.player_bullet_list:
            _bullet.draw()
        
        
        # Collision Box 
        if Common.DEBUG:
            pyxel.rectb(self.x + self.col_x, self.y + self.col_y, self.col_w, self.col_h, pyxel.COLOR_GREEN)
