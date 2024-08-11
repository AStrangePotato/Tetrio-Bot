import pyautogui
from . constants import pieceRGB, nextPieceRGB, boardRGB

#!2560x1440!#
currentRegion = (1240, 75, 16, 16)
nextRegion = (1625, 122, 312, 235)
boardRegion = (981, 122, 599, 1196)
#!1920x1080!#
#currentRegion = (930, 56, 16, 16)
#nextRegion = (1219, 92, 312, 235)


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


def pieceState():
    currentPiece = pyautogui.screenshot("currentPiece.png", region=currentRegion)
    curPiece = pieceFromRGB(currentPiece, (8, 8), 0)

    nextPiece = pyautogui.screenshot("nextPiece.png", region=nextRegion)
    nxtPiece = pieceFromRGB(nextPiece, (155, 165), 1)

    return [curPiece, nxtPiece]


def boardState():
    board = [[0,0,0,0,0,0,0,0,0,0] for i in range(20)]
    boardSS = pyautogui.screenshot("boardState.png", region=boardRegion)

    for y in range(20):
        for x in range(10):
            tile = pieceFromRGB(boardSS, (x*60+30, y*60+30), 2)
            if tile is not None:
                board[y][x] = tile
            else:
                board[y][x] = '?'
    return board
