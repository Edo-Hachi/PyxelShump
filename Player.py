import pyxel
import Common

from Bullet import Bullet

ExtNames = ["EXT01", "EXT02", "EXT03", "EXT04"]
ExtMax = len(ExtNames)


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


        self.SprName = "TOP"    #Drawing Sprite Name

        self.ExtIndex = 0
        self.ExtSpr = "EXT01"  # Exhaust Sprite Name

        #self.bullets = []  # Bullet Manage list
        #Bullet

    def update(self):
        #Exhaust Animation
        self.ExtSpr = ExtNames[self.ExtIndex]
        
        self.ExtIndex += 1
        if self.ExtIndex >= ExtMax:
            self.ExtIndex = 0


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

        # 移動
        self.x += dx * self.speed
        self.y += dy * self.speed

        # 画面端での境界チェック
        self.x = max(0, min(self.x, Common.WIN_WIDTH - self.width))
        self.y = max(0, min(self.y, Common.WIN_HEIGHT - (self.height+8)))
        
        #弾の発射
        if pyxel.btnp(pyxel.KEY_SPACE):

            pyxel.play(0, 0)  # 効果音再生

            Common.player_bullet_list.append(Bullet(self.x-4, self.y-2, 8, 8)) # 弾の情報をリストに追加
            Common.player_bullet_list.append(Bullet(self.x+4, self.y-2, 8, 8)) # 弾の情報をリストに追加
            
        # 弾の更新と削除
        for _bullet in Common.player_bullet_list:
            _bullet.update()
        Common.player_bullet_list = [b for b in Common.player_bullet_list if b.active]

        #プレイヤーと敵との当たり判定
        for _enemy in Common.enemy_list:
            if self.col_active and _enemy.active:

                if Common.check_collision(self.x + self.col_x, self.y + self.col_y, self.col_w, self.col_h,
                                       _enemy.x + _enemy.col_x, _enemy.y + _enemy.col_y, _enemy.col_w, _enemy.col_h):

                # if (self.x + self.col_x < _enemy.x + _enemy.col_x + _enemy.col_w and
                #     self.x + self.col_x + self.col_w > _enemy.x + _enemy.col_x and
                #     self.y + self.col_y < _enemy.y + _enemy.col_y + _enemy.col_h and
                #     self.y + self.col_y + self.col_h > _enemy.y + _enemy.col_y):
                    #print("Collision")
                    Common.GameState = Common.STATE_GAMEOVER
                    #Common.player_bullet_list.remove(_bullet)
                    #Common.enemy_list.remove(_enemy)
                    #break
        #count = len(Common.player_bullet_list)
        #print(count)

    
    def draw(self):

        #Player Ship
        pyxel.blt(self.x, self.y, Common.TILE_BANK0,
            Common.SprList[self.SprName].x, Common.SprList[self.SprName].y, self.width, self.height, pyxel.COLOR_BLACK)

        #Exhaust
        pyxel.blt(self.x, self.y+8, Common.TILE_BANK0,
            #Common.SprList[ExtNames[self.ExtIndex]].x, Common.SprList[ExtNames[self.ExtIndex]].y, self.width, self.height, pyxel.COLOR_BLACK)
            Common.SprList[self.ExtSpr].x, Common.SprList[self.ExtSpr].y, self.width, self.height, pyxel.COLOR_BLACK)

        # Collision Box
        pyxel.rectb(self.x + self.col_x, self.y + self.col_y, self.col_w, self.col_h, pyxel.COLOR_GREEN)


        # 描画
        for _bullet in Common.player_bullet_list:
            _bullet.draw()
        
