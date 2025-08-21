import copy
import time
import keyboard
import random

from lib import detect, heuristic, move, visuals
from lib.constants import pieces, weights, PIECE_DELAY

#Gets key of a value in a dict.
def getKey(pieceArr):
    for k, v in pieces.items():
        if pieceArr == v:
            return k

#Returns the lowest tile in a tetromino.
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

#Simulates dropping a piece and returns the new board.
def drop(piece, pos, board):
    #if board[0][pos] != 0 or board[0][pos] is not None:
        #return "Invalid drop location. Spot filled."
    
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

#Returns [score, rotation, position].
def searchDrops(boardMaster, piece, weights):
    best = [-float("inf"), -1, -1] 
    if piece is None:
        return best
    
    for rotation in range(len(piece)):
        maxPos = 11 - len(piece[rotation][0])
        for pos in range(maxPos):
            boardSnapshot = copy.deepcopy(boardMaster) #new instance
            simulBoard = drop(piece[rotation], pos, boardSnapshot)
            score = heuristic.analyze(simulBoard, weights)

            if score > best[0]:
                best = [score, rotation, pos]

            simulBoard = boardSnapshot #revert instance

    return best

#Boolean if the top rows of a board are filled.
def gameOver(board):
    for tile in "jlszoti":
        if tile in board[2]:
            return True
    return False

def play(duration=float("inf"), weights=weights):
    #Setup - wait for first piece to appear
    while True:
        pieceInfo = detect.pieceState()
        if pieceInfo[0] is not None:
            move.hold()
            held = pieces[pieceInfo[0]]
            current = pieces[pieceInfo[1]]
            startTime = time.time()
            break


    while time.time() < startTime + duration:
        if keyboard.is_pressed('q'):
            break

        #!GRAB STATE!#
        boardMaster = detect.boardState()
        pieceInfo = detect.pieceState()
        current, next = pieces[pieceInfo[0]], pieces[pieceInfo[1]]

        #!TERMINATE ROLLOUT!#
        if gameOver(boardMaster):
            break
        
        #!SIMULATE DROPS!#
        if current is not None:
            best_current = searchDrops(boardMaster, current, weights)
            best_hold = searchDrops(boardMaster, held, weights)

            #After simulation
            if best_current[0] >= best_hold[0]:
                move.place(best_current[1], best_current[2], getKey(current))
            else:
                move.hold()
                move.place(best_hold[1], best_hold[2], getKey(held))
                held = current #current piece goes to hold

    
if __name__ == "__main__":
    play()