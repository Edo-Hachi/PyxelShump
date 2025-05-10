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
# Title State ----------------------------------------

# Playing State ----------------------------------------

def update_playing(self):
    self.star_manager.update()
    self.player.update()


    #debug code Enemy Spawn
    if Common.GameTimer % 100 == 0:
        enemy_x = random.randint(0, Common.WIN_WIDTH - 8)
        enemy_y = 8
        _Enemy = Enemy(enemy_x, enemy_y, 8, 8, 2, 100)

        Common.enemy_list.append(_Enemy)

    #敵の更新処理
    for _e in Common.enemy_list:
            _e.update()


    #ガベコレ(自弾とかに当たってたら消す)
    Common.enemy_list = [e for e in Common.enemy_list if e.active]



def draw_playing(self):
    pyxel.cls(pyxel.COLOR_NAVY)

    self.star_manager.draw()
    self.player.draw()

    for _e in Common.enemy_list:
        _e.draw()
    
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
        Common.explode_manager.update()
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
        Common.explode_manager.draw()
        #ばくはつだーーーーーーーーーーーーーーーーーーーー

App()
