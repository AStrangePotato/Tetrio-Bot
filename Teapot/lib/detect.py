import dxcam
from . constants import pieceRGB, nextPieceRGB, boardRGB


if False:
    #!1920x1080!#
    currentRegion = (930, 56, 946, 72)
    nextRegion = (1185, 95, 1417, 272)
    boardRegion = (737, 94, 1183, 989)

else:
    #!2560x1440!#
    currentRegion = (1240, 75, 1256, 91) #region = (left, top, right, bottom)
    nextRegion = (1625, 122, 1937, 357)
    boardRegion = (980, 122, 1580, 1318)


camera = dxcam.create()

def getKey(val, dictionary):
    for k, v in dictionary.items():
        #no clue why this is here
        if type(v) == tuple:
            if v == val:
                return k
        elif type(v) == list:
            for tup in v:
                if tup == val:
                    return k

def pieceFromRGB(image, coord, dictLookUp):
    try:
        rgb = tuple(image[coord[1]][coord[0]])
        return getKey(rgb, dictLookUp)
    except: #dxcam null
        return None

def pieceState():
    #From dxcam docs:
    #It is worth noting that .grab will return None if there is no new frame since the 
    # last time you called .grab. Usually it means there's nothing new to render since 
    # (E.g. You are idling).

    currentPiece = camera.grab(region=currentRegion)
    curPiece = pieceFromRGB(currentPiece, (8, 8), pieceRGB)

    nextPiece = camera.grab(region=nextRegion)
    nxtPiece = pieceFromRGB(nextPiece, (155, 165), nextPieceRGB)

    return [curPiece, nxtPiece]


def boardState():
    board = [[0,0,0,0,0,0,0,0,0,0] for i in range(20)]
    boardSS = camera.grab(region=boardRegion)

    tileSize = (boardRegion[2]-boardRegion[0]) // 10

    for y in range(20):
        for x in range(10):
            tile = pieceFromRGB(boardSS, (x*tileSize + tileSize//2, y*tileSize + tileSize//2), boardRGB)
            if tile is not None:
                board[y][x] = tile
            else:
                board[y][x] = '?'
                
    return board

