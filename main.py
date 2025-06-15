import pyxel
import random

import Common
from Enemy import Enemy, ENEMY_MOVE_SPEED, MOVE_THRESHOLD
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

    pyxel.text(40, 50, "Pyxel Shumup", 7)
    pyxel.text(25, 70, "Press SPACE to Start", 7)
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
                sprite_num = Common.get_current_stage_map()[_y][_x]
                _Enemy = Enemy(enemy_x, enemy_y, 8, 8, 2, 100, sprite_num)
                Common.enemy_list.append(_Enemy)
        
        Common.GameStateSub = Common.STATE_PLAYING_FIGHT

    # --- 弾の移動処理（プレイヤーの弾） ---
    for _b in Common.player_bullet_list:
        _b.update()

    # --- 敵の弾の移動処理 ---
    for _b in Common.enemy_bullet_list:
        _b.update()

    # ステージクリア時の処理
    if Common.GameStateSub == Common.STATE_PLAYING_STAGE_CLEAR:
        if pyxel.btn(pyxel.KEY_Z):
            Common.CURRENT_STAGE += 1
            Common.GameStateSub = Common.STATE_PLAYING_ENEMY_SPAWN
        return

    # --- 敵の移動処理だけを行う（衝突判定は外す） ---
    # グループ移動の更新
    Common.enemy_group_x += ENEMY_MOVE_SPEED * Common.enemy_move_direction
    
    # 移動量が閾値を超えたら整数値で移動
    if abs(Common.enemy_group_x) >= MOVE_THRESHOLD:
        move_amount = int(Common.enemy_group_x)
        Common.enemy_group_x -= move_amount
        
        # グループ全体の移動
        for enemy in Common.enemy_list:
            if enemy.active:
                enemy.x += move_amount

        # 画面端での方向転換チェック
        if Common.enemy_move_direction == Common.ENEMY_MOVE_RIGHT:
            # 右端のエネミーを探す
            rightmost_x = max(enemy.x for enemy in Common.enemy_list if enemy.active)
            if rightmost_x + 8 >= Common.WIN_WIDTH:  # 8はエネミーの幅
                Common.enemy_move_direction = Common.ENEMY_MOVE_LEFT
        else:
            # 左端のエネミーを探す
            leftmost_x = min(enemy.x for enemy in Common.enemy_list if enemy.active)
            if leftmost_x <= 0:
                Common.enemy_move_direction = Common.ENEMY_MOVE_RIGHT

    for _e in Common.enemy_list:
        _e.update()

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

    # --- 衝突判定：敵弾 vs プレイヤー ---
    for bullet in Common.enemy_bullet_list:
        if not bullet.active:
            continue  # 非アクティブな弾はスキップ

        # プレイヤーとの衝突チェック
        if Common.check_collision(
            bullet.x + bullet.col_x, bullet.y + bullet.col_y, bullet.col_w, bullet.col_h,
            self.player.x + self.player.col_x, self.player.y + self.player.col_y, 
            self.player.col_w, self.player.col_h
        ):
            bullet.active = False  # 弾を消す
            self.player.on_hit()  # プレイヤーのヒット処理

    # --- 衝突判定：プレイヤー vs 敵 ---
    for enemy in Common.enemy_list:
        if not enemy.active:
            continue  # 非アクティブな敵はスキップ

        # プレイヤーとの衝突チェック
        if Common.check_collision(
            self.player.x + self.player.col_x, self.player.y + self.player.col_y,
            self.player.col_w, self.player.col_h,
            enemy.x + enemy.col_x, enemy.y + enemy.col_y,
            enemy.col_w, enemy.col_h
        ):
            self.player.on_hit()  # プレイヤーのヒット処理

    # --- ガベージコレクション（死んだ敵、自弾も除去） ---
    Common.enemy_list = [e for e in Common.enemy_list if e.active]
    Common.player_bullet_list = [b for b in Common.player_bullet_list if b.active]
    Common.enemy_bullet_list = [b for b in Common.enemy_bullet_list if b.active]

    Common.check_stage_clear()

def draw_playing(self):

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
    
    # 敵の弾の描画
    for _b in Common.enemy_bullet_list:
        _b.draw()
    
    #爆発描画ーーーーーーーーーーーーーーーーーーーー
    Common.explode_manager.draw()
    #ばくはつだーーーーーーーーーーーーーーーーーーーー

    #Draw HUD
    pyxel.camera(0, 0)      
    pyxel.text(8, 0, "Score: " + str(Common.Score), 7)

    # ステージクリア表示
    if Common.GameStateSub == Common.STATE_PLAYING_STAGE_CLEAR:
        pyxel.text(40, 50, "Stage Clear!", 7)
        pyxel.text(20, 70, "Press Z to continue", 7)

class App:
    def __init__(self):
        pyxel.init(Common.WIN_WIDTH, Common.WIN_HEIGHT, title="Mini Shooter", display_scale=5, fps=60)
        pyxel.load("my_resource.pyxres")

        Common.GameState = Common.STATE_TITLE

        #Bg Stars
        self.star_manager = StarManager(count=100)        

        #Player Star Ship
        self.player = Player(64-4, 108)

        Common.Score = 10
        Common.HighScore = 100

        pyxel.run(self.update, self.draw)
        

    def update(self):
        Common.GameTimer += 1

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


App()
