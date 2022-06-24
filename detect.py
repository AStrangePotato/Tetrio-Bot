import pyautogui
import numpy as np
import PIL
import time

#6350k, 80% dimmer, current piece
pieceRGB = {"s":(86,234,80),  #green
            "z":(255,83,115), #red
            "j":(0,115,230),  #blue
            "l":(255,167,26), #orange
            "o":(255,255,56), #yellow
            "t":(187,51,203), #purple
            "i":(64,221,255)} #light blue

nextPieceRGB = {"s":(81,184,77),  #green
                "z":(235,79,101), #red
                "j":(17,101,181),  #blue
                "l":(243,137,39), #orange
                "o":(246,208,60), #yellow
                "t":(151,57,162), #purple
                "i":(66,175,225)}

def getKey(val, next):
    if next:
        for k, v in nextPieceRGB.items():
            if v == val:
                return k
    else:
        for k, v in pieceRGB.items():
            if v == val:
                return k

def pieceFromRGB(image, coord, next):
    image = image.convert("RGB")
    rgb = image.getpixel((coord))
    return getKey(rgb, next)
#2560x1440
currentRegion = (1240, 75, 16, 16)
nextRegion = (1625, 122, 312, 235)
#1920x1080
#currentRegion = (930, 56, 16, 16)
#nextRegion = (1219, 92, 312, 235)

def pieceState():
    currentPiece = pyautogui.screenshot("currentPiece.png", region=currentRegion)
    curPiece = pieceFromRGB(currentPiece, (8, 8), False)

    nextPiece = pyautogui.screenshot("nextPiece.png", region=nextRegion)
    nxtPiece = pieceFromRGB(nextPiece, (155, 165), True)

    return [curPiece, nxtPiece]

