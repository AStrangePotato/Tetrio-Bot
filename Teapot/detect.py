import pyautogui
import numpy as np
import PIL
import time
from visuals import draw

#6350k, 80% dimmer, current piece
pieceRGB = {"s":(86,234,80),  #green
            "z":(255,83,115), #red
            "j":(0,115,230),  #blue
            "l":(255,167,26), #orange
            "o":(255,255,56), #yellow
            "t":(187,51,203), #purple
            "i":(64,221,255) #light blue
            }

nextPieceRGB = {"s":(81,184,77),  #green
                "z":(235,79,101), #red
                "j":(17,101,181), #blue
                "l":(243,137,39), #orange
                "o":(246,208,60), #yellow
                "t":(151,57,162), #purple
                "i":(66,175,225) #light blue
                }

boardRGB = {"s":[(81,184,77), (86,234,80)],  
            "z":[(235,79,101),(255,83,115)], 
            "j":[(17,101,181),(0,115,230)], 
            "l":[(243,137,39),(255,167,26)], 
            "o":[(246,208,60),(255,255,56)], 
            "t":[(151,57,162),(187,51,203)], 
            "i":[(66,175,225),(64,221,255)], 

            "x":(134,134,134),
            0:(0,0,0)}

def getKey(val, dict):
    if dict == 0:
        dictionary = pieceRGB
    elif dict == 1:
        dictionary = nextPieceRGB
    elif dict == 2:
        dictionary = boardRGB

    for k, v in dictionary.items():
        if type(v) == tuple:
            if v == val:
                return k
        elif type(v) == list:
            for tup in v:
                if tup == val:
                    return k

def pieceFromRGB(image, coord, dictLookUp):
    image = image.convert("RGB")
    rgb = image.getpixel((coord))
    return getKey(rgb, dictLookUp)

#!2560x1440!#
currentRegion = (1240, 75, 16, 16)
nextRegion = (1625, 122, 312, 235)
boardRegion = (981, 122, 599, 1196)
#!1920x1080!#
#currentRegion = (930, 56, 16, 16)
#nextRegion = (1219, 92, 312, 235)

board = [[0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0]]

def pieceState():
    currentPiece = pyautogui.screenshot("currentPiece.png", region=currentRegion)
    curPiece = pieceFromRGB(currentPiece, (8, 8), 0)

    nextPiece = pyautogui.screenshot("nextPiece.png", region=nextRegion)
    nxtPiece = pieceFromRGB(nextPiece, (155, 165), 1)

    return [curPiece, nxtPiece]


def boardState():
    boardSS = pyautogui.screenshot("boardState.png", region=boardRegion)

    for y in range(20):
        for x in range(10):
            tile = pieceFromRGB(boardSS, (x*60+30, y*60+30), 2)
            if tile is not None:
                board[y][x] = tile
            else:
                board[y][x] = '?'
    return board
