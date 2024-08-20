import copy
import time
import keyboard

from lib import detect, heuristic, move, visuals
from lib.constants import pieces




def getKey(pieceArr):
    for k, v in pieces.items():
        if pieceArr == v:
            return k

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


#Returns [score, rotation, position]
def searchDrops(boardMaster, piece, weights):
    best = [-float("inf"), -1, -1] 

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


def main(weights=[-0.530213, 0.760667, -10.4, -0.420690, -30.474278, -2.042069, -0.420420]):
    #Setup - wait for first piece to appear
    while True:
        pieceInfo = detect.pieceState()
        if pieceInfo[0] is not None:
            move.hold()
            held = pieces[pieceInfo[0]]
            current = pieces[pieceInfo[1]]
            break


    while True:
        time.sleep(0.03) #good delay (too fast for public lobbies - will get kicked)
        if keyboard.is_pressed('q'):
            break
        
        #!GRAB STATE!#
        boardMaster = detect.boardState()
        pieceInfo = detect.pieceState()
        current, next = pieces[pieceInfo[0]], pieces[pieceInfo[1]]

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

            

    visuals.draw(boardMaster)

if __name__ == "__main__":
    main()