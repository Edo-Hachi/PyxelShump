import pyxel

TILE_SIZE = 8
TILES_PER_ROW = 16
TILE_BANK0 = 0
TILE_BANK1 = 1
TILE_BANK2 = 2


class App:
    def __init__(self):
        pyxel.init(160, 120, title="Mini Shooter")
        self.x = 72  # 自機の初期X位置
        self.y = 100  # 自機の初期Y位置
        pyxel.run(self.update, self.draw)
        

    def update(self):

        if pyxel.btn(pyxel.KEY_LEFT):
            self.x = max(self.x - 2, 0)
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x = min(self.x + 2, pyxel.width - 8)

        if pyxel.btnp(pyxel.KEY_SPACE):  # 発射キー（1回押し）
            self.bullets.append((self.x + 4, self.y))

        # 弾を上に移動
        #self.bullets = [(bx, by - 4) for bx, by in self.bullets if by > 0]

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(self.x, self.y, 8, 8, 9)  # 自機を描画（青）
        # for bx, by in self.bullets:
        #     pyxel.rect(bx, by, 1, 4, 7)  # 弾は白
App()
