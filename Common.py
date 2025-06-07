from collections import namedtuple
from ExplodeManager import ExpMan
from enum import Enum

VERSION = "0.1.2"

DEBUG = False #or False

#Window size
WIN_WIDTH = 128
WIN_HEIGHT = 128

#Sprite banks
TILE_BANK0 = 0
TILE_BANK1 = 1
TILE_BANK2 = 2

#State IDs
STATE_TITLE = 0
STATE_PLAYING = 1
STATE_GAMEOVER = 2
STATE_PAUSE = 3

#Camera Shake
ShakeTimer = 0
ShakeStrength = 10
StopTimer = 0

STOP_TIME = 20  # Stop Time
SHAKE_TIME = 10  # Camera Shake Time

HighScore = 0
Score = 0
GameState = STATE_TITLE

GameTimer = 0

#Sprite Collision List
enemy_list = []
enemy_bullet_list = []
player_bullet_list = []

#パーティクル管理オブジェクト
explode_manager = ExpMan()

def check_collision(x1, y1, w1, h1, x2, y2, w2, h2):
    # 各辺の位置を計算
    left1   = x1
    right1  = x1 + w1
    top1    = y1
    bottom1 = y1 + h1

    left2   = x2
    right2  = x2 + w2
    top2    = y2
    bottom2 = y2 + h2

    # 衝突しているかを確認
    is_collision = (
        left1   < right2 and
        right1  > left2 and
        top1    < bottom2 and
        bottom1 > top2
    )

    return is_collision


#Sprite Location List
# 8x8 sprites
SpIdx =  namedtuple("SprIdx", ["x", "y"])
SprList = {
    'NULL' : SpIdx(0, 0),  # NULL
    "TOP" : SpIdx(8, 0),  # TOP
    "LEFT" : SpIdx(16, 0),  # LEFT
    "RIGHT" : SpIdx(24, 0),  # RIGHT
    "NULL" : SpIdx(32, 0),   # NULL
    


    "BULLET01" : SpIdx(40, 0),  # BULLET
    "BULLET02" : SpIdx(48, 0),  

    "EXT01" : SpIdx(56, 0), # Ship Exhaust
    "EXT02" : SpIdx(64, 0), # Ship Exhaust
    "EXT03" : SpIdx(72, 0), # Ship Exhaust
    "EXT04" : SpIdx(80, 0), # Ship Exhaust

    "MUZL01" : SpIdx(88, 0),  #MuzzleFlash01
    "MUZL02" : SpIdx(96, 0),  #MuzzleFlash02
    "MUZL03" : SpIdx(104, 0),  #MuzzleFlash03
    "NULL" : SpIdx(112, 0),
    "NULL" : SpIdx(120, 0),

    "NULL" : SpIdx(0, 8),    #NULL
    
    "ENEMY01_0" : SpIdx(8, 8),    #Enemy01_0
    "ENEMY01_1" : SpIdx(16, 8),   #Enemy01_1
    "ENEMY01_2" : SpIdx(24, 8),   #Enemy01_2
    "ENEMY01_3" : SpIdx(32, 8),   #Enemy01_3

    "ENEMY02_0" : SpIdx(40, 8),   #Enemy02_0
    "ENEMY02_1" : SpIdx(48, 8),   #Enemy02_0
    "ENEMY02_2" : SpIdx(56, 8),   #Enemy02_0
    "ENEMY02_3" : SpIdx(64, 8),   #Enemy02_0

    "ENEMY03_0" : SpIdx(72, 8),   #Enemy03_0
    "ENEMY03_1" : SpIdx(80, 8),   #Enemy03_1
    "ENEMY03_2" : SpIdx(88, 8),   #Enemy03_2
    "ENEMY03_3" : SpIdx(96, 8),   #Enemy03_3

    "ENEMY04_0" : SpIdx(104, 8),   #Enemy04_0
    "ENEMY04_1" : SpIdx(112, 8),   #Enemy04_1
    "ENEMY04_2" : SpIdx(120, 8),   #Enemy04_2
    "ENEMY04_3" : SpIdx(128, 8),   #Enemy04_3

    "ENEMY05_0" : SpIdx(136, 8),   #Enemy05_0
    "ENEMY05_1" : SpIdx(144, 8),   #Enemy05_1
    "ENEMY05_2" : SpIdx(152, 8),   #Enemy05_2
    "ENEMY05_3" : SpIdx(160, 8),   #Enemy05_3


}
