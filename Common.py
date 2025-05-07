#import math
from collections import namedtuple

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


HighScore = 0
Score = 0
GameState = STATE_TITLE


#Sprite Location List
# 8x8 sprites
SpIdx =  namedtuple("SprIdx", ["x", "y"])
SprList = {
    'NULL' : SpIdx(0, 0),  # NULL
    "TOP" : SpIdx(8, 0),  # TOP
    "LEFT" : SpIdx(16, 0),  # LEFT
    "RIGHT" : SpIdx(24, 0),  # RIGHT
    "NULL" : SpIdx(32, 0),   # NULL

    "BULLET" : SpIdx(40, 0),      #BULLET
    "NULL" : SpIdx(48, 0),  

    "EXT01" : SpIdx(56, 0), # Ship Exhaust
    "EXT02" : SpIdx(64, 0),
    "EXT03" : SpIdx(72, 0),
    "EXT04" : SpIdx(80, 0),

    "NULL" : SpIdx(88, 0),
    "NULL" : SpIdx(96, 0),
    "NULL" : SpIdx(104, 0),
    "NULL" : SpIdx(112, 0),
    "NULL" : SpIdx(120, 0),

    "NULL" : SpIdx(0, 8),    #NULL
    "ENEMY01_0" : SpIdx(8, 8),    #Enemy01_0
    "ENEMY01_1" : SpIdx(16, 8),   #Enemy01_1
    "ENEMY01_2" : SpIdx(24, 8),   #Enemy01_2
    "ENEMY01_3" : SpIdx(32, 8),   #Enemy01_3

}

