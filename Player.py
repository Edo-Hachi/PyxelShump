import pyxel
import Common

from Bullet import Bullet

ExtNames = ["EXT01", "EXT02", "EXT03", "EXT04"]
ExtMax = len(ExtNames)


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 2
        self.width = 8
        self.height = 8

        self.SprName = "TOP"    #Drawing Sprite Name

        self.ExtIndex = 0
        self.ExtSpr = "EXT01"  # Exhaust Sprite Name

        self.bullets = []  # Bullet Manage list
        #Bullet

    def update(self):
        #Exhaust Animation
        self.ExtSpr = ExtNames[self.ExtIndex]
        
        self.ExtIndex += 1
        if self.ExtIndex >= ExtMax:
            self.ExtIndex = 0


        dx = 0  #direction
        dy = 0
        self.SprName = "TOP"

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
            self.bullets.append(Bullet(self.x-4, self.y-2))
            self.bullets.append(Bullet(self.x+4, self.y-2))

        # 弾の更新と削除
        for blt in self.bullets:
            blt.update()
        self.bullets = [b for b in self.bullets if b.active]

    def draw(self):

        #Player Ship
        pyxel.blt(self.x, self.y, Common.TILE_BANK0,
            Common.SprList[self.SprName].x, Common.SprList[self.SprName].y, self.width, self.height, pyxel.COLOR_BLACK)

        #Exhaust
        pyxel.blt(self.x, self.y+8, Common.TILE_BANK0,
            #Common.SprList[ExtNames[self.ExtIndex]].x, Common.SprList[ExtNames[self.ExtIndex]].y, self.width, self.height, pyxel.COLOR_BLACK)
            Common.SprList[self.ExtSpr].x, Common.SprList[self.ExtSpr].y, self.width, self.height, pyxel.COLOR_BLACK)

        # 描画
        for blt in self.bullets:
            blt.draw()
