import pyxel
import Common
import random
from ExplodeManager import ExpType
from EnemyBullet import EnemyBullet

ANIM_FRAME = 10
ENEMY_MOVE_SPEED = 0.5  # 移動速度
MOVE_THRESHOLD = 1  # 移動閾値
SHOOT_INTERVAL = 60  # 発射間隔（フレーム）
BASE_SHOOT_CHANCE = 0.10  # 基本発射確率
MAX_SHOOT_CHANCE = 0.30  # 最大発射確率

class Enemy:
    def __init__(self, x, y, w=8, h=8, life=1, score=10, sprite_num=1):
        self.base_x = x  # 初期X座標を保存
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
        self.shoot_timer = random.randint(0, SHOOT_INTERVAL)  # 発射タイマー

    def update(self):
        if Common.StopTimer > 0:
            return

        # 発射処理
        self.shoot_timer -= 1
        if self.shoot_timer <= 0:
            # 残りの敵の数に応じて発射確率を調整
            remaining_enemies = len([e for e in Common.enemy_list if e.active])
            if remaining_enemies > 0:
                # 敵の数が減るほど発射確率が上がる
                shoot_chance = min(
                    BASE_SHOOT_CHANCE + (BASE_SHOOT_CHANCE * (40 - remaining_enemies) / 40),
                    MAX_SHOOT_CHANCE
                )
                if random.random() < shoot_chance:  # 確率で発射
                    Common.enemy_bullet_list.append(
                        EnemyBullet(self.x + 4, self.y + 8)  # エネミーの中心から発射
                    )
            self.shoot_timer = SHOOT_INTERVAL

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
