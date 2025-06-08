import pyxel
import random

import Common
from Enemy import Enemy
from ExplodeManager import ExpType

from StarManager import StarManager
from Player import Player

# Title State ----------------------------------------
def update_title(self):
    self.star_manager.update()
    if pyxel.btn(pyxel.KEY_SPACE):
        Common.GameState = Common.STATE_PLAYING

def draw_title(self):
    
    pyxel.cls(pyxel.COLOR_NAVY)
    self.star_manager.draw()

    pyxel.text(40, 50, "Mini Shooter", 7)
    pyxel.text(40, 70, "Press SPACE to Start", 7)
    pyxel.text(40, 110, "Game Ver:" + str(Common.VERSION), 7)
    pyxel.text(40, 120, "Pyxel Ver:" + str(pyxel.VERSION), 7)

# Title State ----------------------------------------

# Playing State ----------------------------------------

def update_playing(self):

    #爆発エフェクトはヒットストップに含めない
    Common.explode_manager.update()
    
    if Common.StopTimer > 0:
        Common.StopTimer -= 1
        return  

    self.star_manager.update()
    self.player.update()

    #ゲームスタート時の敵スポーン処理
    if Common.GameStateSub == Common.STATE_PLAYING_ENEMY_SPAWN:
        BASEX = 11
        OFSX = 10

        BASEY = 11
        OFSY = 10

        # --- 敵のスポーン処理 ---
        for _y in range(4):
            enemy_y = OFSY + (BASEY * _y)
            for _x in range(10):
                enemy_x = OFSX + (BASEX * _x)
                #enemy_y = 16
                #sprite_num = random.randint(1, Common.MAX_ENEMY_NUM)
                sprite_num = Common.ENEMY_MAP_STG01[_y][_x]
                _Enemy = Enemy(enemy_x, enemy_y, 8, 8, 4, 100, sprite_num)
                Common.enemy_list.append(_Enemy)
        
        Common.GameStateSub = Common.STATE_PLAYING_FIGHT

    # --- 敵の移動処理だけを行う（衝突判定は外す） ---
    for _e in Common.enemy_list:
        _e.update()

    # --- 弾の移動処理（プレイヤーの弾） ---
    for _b in Common.player_bullet_list:
        _b.update()

    # --- 衝突判定：プレイヤー弾 vs 敵 ---
    for bullet in Common.player_bullet_list:
        if not bullet.active:
            continue  # 非アクティブな弾はスキップ

        for enemy in Common.enemy_list:
            if not enemy.active:
                continue  # 非アクティブな敵はスキップ

            # 衝突しているかをチェック
            if Common.check_collision(
                bullet.x + bullet.col_x, bullet.y + bullet.col_y, bullet.col_w, bullet.col_h,
                enemy.x + enemy.col_x, enemy.y + enemy.col_y, enemy.col_w, enemy.col_h
            ):
                enemy.on_hit(bullet)  # ヒット処理（敵のライフ減少、爆発など）

    # --- ガベージコレクション（死んだ敵、自弾も除去） ---
    Common.enemy_list = [e for e in Common.enemy_list if e.active]
    Common.player_bullet_list = [b for b in Common.player_bullet_list if b.active]


def draw_playing(self):

    #爆発描画ーーーーーーーーーーーーーーーーーーーー
    #Common.explode_manager.draw()
    #ばくはつだーーーーーーーーーーーーーーーーーーーー

    if Common.ShakeTimer == 10:
        pyxel.cls(pyxel.COLOR_WHITE)
    else:
        pyxel.cls(pyxel.COLOR_NAVY)


    if Common.ShakeTimer > 0:
        # カメラシェイクの実装
        shake_offset_x = random.randint(-Common.ShakeStrength, Common.ShakeStrength)
        shake_offset_y = random.randint(-Common.ShakeStrength, Common.ShakeStrength)
        pyxel.camera(shake_offset_x, shake_offset_y)

        Common.ShakeTimer -= 1
    else:
        pyxel.camera(0, 0)  

    self.star_manager.draw()

    self.player.draw()

    for _e in Common.enemy_list:
        _e.draw()
    
    #爆発描画ーーーーーーーーーーーーーーーーーーーー
    Common.explode_manager.draw()
    #ばくはつだーーーーーーーーーーーーーーーーーーーー

    #Draw HUD
    pyxel.camera(0, 0)      
    pyxel.text(8, 0, "Score: " + str(Common.Score), 7)

class App:
    def __init__(self):
        pyxel.init(Common.WIN_WIDTH, Common.WIN_HEIGHT, title="Mini Shooter", fps=60)
        pyxel.load("my_resource.pyxres")

        Common.GameState = Common.STATE_TITLE
        #self.GameState = Common.GameState

        #Bg Stars
        self.star_manager = StarManager(count=100)        

        #Player Star Ship
        self.player = Player(64-4, 108)

        Common.Score = 10
        Common.HighScore = 100

        pyxel.run(self.update, self.draw)
        

    def update(self):
        Common.GameTimer += 1

        #ばくはつだーーーーーーーーーーーーーーーーーーーー
        #爆発パーティクルのテストコード
        # if pyxel.btn(pyxel.KEY_Z):
        #     Common.explode_manager.spawn_explosion(50, 50, 20, ExpType.CIRCLE)
            #self.Explode_mgr.spawn_explosion(50, 50)
            #print("Z Key Pressed")
        #ばくはつだーーーーーーーーーーーーーーーーーーーー


        match Common.GameState:
        
            case Common.STATE_TITLE:
                update_title(self)
            case Common.STATE_PLAYING:
                update_playing(self)
            case Common.STATE_GAMEOVER:
                #print("Game Over")
                pass     
            case Common.STATE_PAUSE:
                pass

        #Esc Key Down
        if pyxel.btn(pyxel.KEY_ESCAPE):
            pyxel.quit()

        #ばくはつだーーーーーーーーーーーーーーーーーーーー
        #Common.explode_manager.update()
        #ばくはつだーーーーーーーーーーーーーーーーーーーー


        #self.player.update()
     
   
    def draw(self):


        match Common.GameState:
            case Common.STATE_TITLE:
                draw_title(self)
            case Common.STATE_PLAYING:
                draw_playing(self)
            case Common.STATE_GAMEOVER:
                pyxel.text(40, 50, "Game Over", 7)

                pass
            case Common.STATE_PAUSE:
                pass

        #self.Explode_mgr.draw()
        #ばくはつだーーーーーーーーーーーーーーーーーーーー
        #Common.explode_manager.draw()
        #ばくはつだーーーーーーーーーーーーーーーーーーーー

        # カスタムカーソルを描画
        # cursor_x = pyxel.mouse_x
        # cursor_y = pyxel.mouse_y
        # cursor_color = pyxel.frame_count % 16  # カーソルの色を時間とともに変化させる
        #pyxel.rect(cursor_x, cursor_y, 4, 4, cursor_color)  # 4x4のカラフルな四角形のカーソル

App()
