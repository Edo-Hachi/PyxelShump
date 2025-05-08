import pyxel
import random

import Common
from Enemy import Enemy


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
    self.Enemy.update()

    # for _enemy in Common.enemy_list:
    #     if _enemy.active:
    #         if Common.check_collision(self.player.x + self.player.col_x, self.player.y + self.player.col_y, self.player.col_w, self.player.col_h,
    #                                    _enemy.x + _enemy.col_x, _enemy.y + _enemy.col_y, _enemy.col_w, _enemy.col_h):


    #             self.collision_flg = True

                #print("Collision!")

def draw_playing(self):
    pyxel.cls(pyxel.COLOR_NAVY)
    self.star_manager.draw()
    self.player.draw()

    self.Enemy.draw()   
    #draw_enemy(self)

    #pyxel.text(5, 5, f"Score: {Common.Score}", 7)
    #pyxel.text(5, 15, f"High Score: {Common.HighScore}", 7)

    if self.collision_flg == True:
        pyxel.text(5, 5, "Hit", 7)
        self.collision_flg = False


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

        #debug code
        #self.enemy_spr = 0
        self.enemy_x = 64
        self.enemy_y = 32
        self.Enemy = Enemy(self.enemy_x, self.enemy_y, 8, 8)

        Common.enemy_list.append(self.Enemy)
        

        self.collision_flg = False

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

App()
