import dxcam
from PIL import Image
import pytesseract

from . constants import pieceRGB, nextPieceRGB, boardRGB
from . constants import currentRegion, nextRegion, boardRegion

camera = dxcam.create()
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


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
            tile = pieceFromRGB(boardSS, (x*tileSize + tileSize//3, y*tileSize + tileSize//3), boardRGB)
            if tile is not None:
                board[y][x] = tile
            else:
                board[y][x] = '?'
                
    return board

def get_digits(image):
    image = Image.fromarray(image)
    text = pytesseract.image_to_string(image, config='outputbase digits --psm 6').rstrip()

    if text[-3] != ".":
        text = text[:-2] + "." + text[-2:]
    
    return text

def get():
    grab = camera.grab(region=(1590, 1140, 1590+285, 1140+80))
    num = get_digits(grab)

    print(num)