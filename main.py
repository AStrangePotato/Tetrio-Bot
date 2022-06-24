import numpy as np
import detect
import copy
import heuristic as hr
from move import *
import time
import keyboard
import random


time.sleep(3)

pieceRGB = {"s":(86,234,80),  #green
            "z":(255,83,115), #red
            "j":(0,115,230),  #blue
            "l":(255,167,26), #orange
            "o":(255,255,56), #yellow
            "t":(187,51,203), #purple
            "i":(64,221,255)} #light blue

class colors:
    lime = '\x1b[38;2;86;234;80m'
    red = '\x1b[38;2;255;83;115m'
    lblue = '\x1b[38;2;64;221;255m'
    magenta = '\x1b[38;2;187;51;203m'
    yellow = '\x1b[38;2;255;255;56m'
    blue = '\x1b[38;2;0;115;230m'
    orange = '\x1b[38;2;255;167;26m'
    reset = "\u001b[37m"
    

pieces = {
            'z':[[['z', 'z', 0], [0, 'z', 'z']], [[0, 0, 'z'], [0, 'z', 'z'], [0, 'z', 0]]],
            's':[[[0, 's', 's'], ['s', 's', 0]], [['s', 0, 0], ['s', 's', 0], [0, 's', 0]]],
            'j':[[['j', 0, 0], ['j', 'j', 'j']], [['j', 'j'], ['j', 0], ['j', 0]], [['j', 'j', 'j'], [0, 0, 'j']], [[0, 'j'], [0, 'j'], ['j', 'j']]],
            'l':[[[0, 0, 'l'], ['l', 'l', 'l']], [['l', 0], ['l', 0], ['l', 'l']], [['l', 'l', 'l'], ['l', 0, 0]], [['l', 'l'], [0, 'l'], [0, 'l']]],
            'i':[[['i', 'i', 'i', 'i']], [['i'], ['i'], ['i'], ['i']]],
            't':[[[0, 't', 0], ['t', 't', 't']], [['t', 0], ['t', 't'], ['t', 0]], [['t', 't', 't'], [0, 't', 0]], [[0, 't'], ['t', 't'], [0, 't']]],
            'o':[[['o', 'o'], ['o', 'o']]],
            None:None }

boardMaster = [[0,0,0,0,0,0,0,0,0,0],
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

def getKey(pieceArr):
    for k, v in pieces.items():
        if pieceArr == v:
            return k
        
def getColor(pieceType):
    match pieceType:
        case 0:
            return colors.reset
        case 's':
            return colors.lime
        case 'z':
            return colors.red
        case 'j':
            return colors.blue
        case 'l':
            return colors.orange
        case 'o':
            return colors.yellow
        case 't':
            return colors.magenta
        case 'i':
            return colors.lblue
     
def shape(arr):
    return (len(arr), len(arr[0]))

def lowestBlocks(piece):
    lowestBlocks = []

    columns = []
    for i in range(len(piece[0])):
        columns.append([row[i] for row in piece])

    for c in range(len(columns)):
        for lowest in range(len(columns[c])-1,-1,-1): #start from the bottom and go up until non empty tile is found
            if piece[lowest][c] != 0:
                lowestBlocks.append([lowest, c])
                break
            
    return lowestBlocks
            
def drop(piece, pos, board):
    if board[0][pos] != 0:
        return "Invalid drop location. Spot filled."
    
    altitude = 1
    lowestTiles = lowestBlocks(piece)
    
    falling = True
    while falling:
        validDrop = True
        try:
            for tile in lowestTiles:
                belowY, belowX = tile[0] + altitude, tile[1] + pos
                if belowY > 19 or board[belowY][belowX] != 0:
                    validDrop = False
        except:
            print("hit bottom")

        if validDrop:
            #clear old
            for line in range(len(piece)):
                for tile in range(len(piece[line])):
                    if piece[line][tile] != 0:
                        board[line + altitude - 1][tile + pos] = 0
            #add new
            for line in range(len(piece)):
                for tile in range(len(piece[line])):
                    if piece[line][tile] != 0:
                        board[line + altitude][tile+pos] = piece[line][tile]
    
        else:
            falling = False

        altitude += 1
    return board

def draw(board):
    print("\n")
    n = 0
    print("   ", end="")
    for i in range(10):
        print(str(i) + " ",end="")
    print("\r")
    for line in board:
        if n < 10:
            print(str(n) + "  ", end="")
        else:
            print(str(n) + " ", end="")

        for tile in line:
            print(getColor(tile) + str(tile) + " " +colors.reset, end="")
        print("\r")

        n += 1

def lineClear(board):
    for row in range(20):
        cleared = True
        for tile in range(10):
            if board[row][tile] == 0:
                cleared = False
                break
                
        if cleared:
            board.pop(row)
            board.insert(0, [0,0,0,0,0,0,0,0,0,0])


while True:
    pieceInfo = detect.pieceState()
    if pieceInfo[0] is not None:
        hold()
        held = pieces[pieceInfo[0]]
        current = pieces[pieceInfo[1]]
        break
time.sleep(0.1)
firstPiece = True
while True:
    if keyboard.is_pressed('q'):
        break

    pieceInfo = detect.pieceState()
    currentString = pieceInfo[0]
    if not firstPiece:
        current, next = pieces[pieceInfo[0]], pieces[pieceInfo[1]]
    elif firstPiece:
        firstPiece = False

    best = [-99999, False, 0,0] #(score, held t/f, [rotation, position])

    #!SIMULATE DROPS!#
    if current is not None:
        for rotation in range(len(current)):
            maxPos = 11 - len(current[rotation][0])
            for pos in range(maxPos):
                boardSnapshot = copy.deepcopy(boardMaster) #new instance
                simulBoard = drop(current[rotation], pos, boardSnapshot)
                score = hr.analyze(simulBoard)

                if score == best[0] and random.uniform(0,1) < 0.35: #left bias
                    best = [score, False, rotation, pos] 
                if score > best[0]:
                    best = [score, False, rotation, pos]          

                simulBoard = boardSnapshot #revert instance
        
        #check held piece drops
        for rotation in range(len(held)):
            maxPos = 11 - len(held[rotation][0])
            for pos in range(maxPos):
                boardSnapshot = copy.deepcopy(boardMaster) #new instance
                simulBoard = drop(held[rotation], pos, boardSnapshot)
                score = hr.analyze(simulBoard)

                if score == best[0] and random.uniform(0,1) < 0.3: #left bias
                    best = [score, True, rotation, pos] 
                if score > best[0]:
                    best = [score, True, rotation, pos]     

                simulBoard = boardSnapshot #revert instance
                
        #after simulation
        bestRot = best[2]
        bestPos = best[3]
        if best[1]: #if the optimal score was achieved with held piece
            hold()
            held, current = current, held

        drop(current[bestRot], bestPos, boardMaster)
        place(bestRot, bestPos, getKey(current))

        lineClear(boardMaster)
        #print(bestRot, bestPos, currentString)
        time.sleep(0.1)

draw(boardMaster)