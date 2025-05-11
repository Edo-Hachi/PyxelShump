import pyxel
import random

import Common
from Enemy import Enemy
#from ExplodeManager import ExplodeManager


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
    pyxel.text(50, 110, "Game Ver:" + str(Common.VERSION), 7)
    pyxel.text(50, 120, "Pyxel Ver:" + str(pyxel.VERSION), 7)

# Title State ----------------------------------------

# Playing State ----------------------------------------

def update_playing(self):
    self.star_manager.update()
    self.player.update()

    # --- デバッグ用敵スポーン ---
    if Common.GameTimer % 50 == 0:
        enemy_x = random.randint(0, Common.WIN_WIDTH - 8)
        enemy_y = 8
        _Enemy = Enemy(enemy_x, enemy_y, 8, 8, 2, 100)
        Common.enemy_list.append(_Enemy)

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

    #ばくはつだーーーーーーーーーーーーーーーーーーーー
    Common.explode_manager.update()
    #ばくはつだーーーーーーーーーーーーーーーーーーーー


def draw_playing(self):
    pyxel.cls(pyxel.COLOR_NAVY)

    self.star_manager.draw()
    self.player.draw()

    for _e in Common.enemy_list:
        _e.draw()
    
    #ばくはつだーーーーーーーーーーーーーーーーーーーー
    Common.explode_manager.draw()
    #ばくはつだーーーーーーーーーーーーーーーーーーーー

    #Draw HUD
    pyxel.text(8, 0, "Score: " + str(Common.Score), 7)


# Playing State ----------------------------------------




class App:
    def __init__(self):
        pyxel.init(Common.WIN_WIDTH, Common.WIN_HEIGHT, title="Mini Shooter", fps=60)
        pyxel.load("my_resource.pyxres")

        Common.GameState = Common.STATE_TITLE
        #self.GameState = Common.GameState

        #Bg Stars
        self.star_manager = StarManager(count=100)        

        #Player Star Ship
        self.player = Player(64, 64)

        Common.Score = 10
        Common.HighScore = 100

        #爆発パーティクル(Test)
        #self.Explode_mgr = ExplodeManager()

        

        #self.collision_flg = False

        pyxel.run(self.update, self.draw)
        

    def update(self):
        Common.GameTimer += 1

        #ばくはつだーーーーーーーーーーーーーーーーーーーー
        if pyxel.btn(pyxel.KEY_Z):
            Common.explode_manager.spawn_explosion(50,50)
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

App()
