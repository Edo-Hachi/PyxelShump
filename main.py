import pyxel
import random

import Common
from StarManager import StarManager
from Player import Player

def update_title(self):
    self.star_manager.update()
    if pyxel.btn(pyxel.KEY_SPACE):
        Common.GameState = Common.STATE_PLAYING

def draw_title(self):
    
    pyxel.cls(pyxel.COLOR_NAVY)
    self.star_manager.draw()

    pyxel.text(40, 50, "Mini Shooter", 7)
    pyxel.text(40, 70, "Press SPACE to Start", 7)

def update_playing(self):
    self.star_manager.update()
    self.player.update()


def draw_enemy(self):
    #animate enemy sprite
    #sprname = basename + str(_enemy_spr)
    self.enemy_spr = (self.enemy_spr + 0.1) % 3.5
    sprname = f"ENEMY01_{round(self.enemy_spr)}"

    pyxel.blt(self.enemy_x, self.enemy_y, Common.TILE_BANK0,
            Common.SprList[sprname].x, Common.SprList[sprname].y, 8, 8, pyxel.COLOR_BLACK)
    
    self.enemy_y += 1
    if self.enemy_y > Common.WIN_HEIGHT:
        self.enemy_y = 0
        self.enemy_x = random.randint(0, Common.WIN_WIDTH - 8)


def draw_playing(self):
    pyxel.cls(pyxel.COLOR_NAVY)
    self.star_manager.draw()
    self.player.draw()

    draw_enemy(self)

    pyxel.text(5, 5, f"Score: {Common.Score}", 7)
    pyxel.text(5, 15, f"High Score: {Common.HighScore}", 7)

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
        self.enemy_spr = 0
        self.enemy_x = 64
        self.enemy_y = 8
        
        pyxel.run(self.update, self.draw)
        

    def update(self):
        match Common.GameState:
        
            case Common.STATE_TITLE:
                update_title(self)
            case Common.STATE_PLAYING:
                update_playing(self)
            case Common.STATE_GAMEOVER:
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
                pass
            case Common.STATE_PAUSE:
                pass

App()
