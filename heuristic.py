def aggregate(board, columns):
    aggregateHeight = 0
    aHM = 1.234
    for i in range(10):
        for j in range(20):
            if board[j][i] != 0: #find first non empty tile in the board and sum to aH
                if j < 6: #downstacking threshold
                    aggregateHeight += (20-j) * aHM - j/10 #reduce tie
                else:
                    aggregateHeight += 20 - j - j/10 #the lower it is the better to reduce tie
                break

    return aggregateHeight


def clearedLines(board):
    clearedLines = 0
    for line in board: #cleared line until detects empty tile
        cleared = True
        for tile in line:
            if tile == 0:
                cleared = False
                break
        if cleared:
            clearedLines += 1
            
    match clearedLines:
        case 4:
            clearedLines += 10 #tetris gucci
        case 3:
            clearedLines *= 0.8 #triple are meh
        case 2:
            clearedLines += 1.5 #doubles are value
        case 1:
            clearedLines *= 0.32 #singles are not value
            
    return clearedLines


def holes(board, columns):
    holes = 0
    for i in range(10):
        col = columns[i]
        for tile in range(len(col)):
            if tile < 19:
                #if current tile is not empty and tile below is empty
                if col[tile+1] == 0 and col[tile] != 0: 
                    holes += 1

    return holes


def bumpiness(board, columns, colHeights):
    bumpiness = 0

    prevH = colHeights[0]
    for h in range(1, len(colHeights)): #get difference between adjacent columns
        bumpiness += abs(prevH - colHeights[h])
        prevH = colHeights[h]
        
    return bumpiness


def blockade(board, columns, colHeights):
    blockade = 0
    holeSpots = []

    for i in range(10):
        for j in range(19, -1, -1):
            if columns[i][j] == 0:
                holeSpots.append(j)
                break
    for i in range(10):
        for j in range(holeSpots[i], -1, -1):
            if columns[i][j] != 0:
                blockade += 1
    return blockade


def tetrisSlot(board, well):
    cleared = 0
    nonClearI = 0
    for i in range(20):
        clr = True
        for j in range(10):
            if board[i][j] == 0:
                clr = False
                break
        if clr:
            cleared += 1
                
    for tile in well:
        if tile != 'i' and tile != 0:
            return 1
        if tile == 'i':
            nonClearI += 1

    if nonClearI > cleared:
        return 0.4
    if nonClearI >= cleared:
        return 0.1

    return 0


def iDependency(board, columns, colHeights):
    iDep = 0

    for i in range(1, 8):
        c, l, r = colHeights[i], colHeights[i-1], colHeights[i+1] #heights of current and adjacent columns
        if l - c >= 3 and r - c >= 3:
            iDep += 1
            
    if colHeights[-2] - colHeights[-1] >= 3:
        iDep += 1
    if colHeights[2] - colHeights[1] >= 3:
        iDep += 1

    return iDep


def analyze(board):
    a = -0.530203 #aggregate
    b =  0.760667 #increase tetris score after mvp
    c = -0.694585 #hole
    d = -0.229412 #bumpiness
    e = -0.174278 #blockade
    f = -4.042069 #tetris well
    g = -0.420420 #i piece dependencies

    colHeights = []
    for i in range(10):
        for j in range(20): #go down from the top and break when tile is detected
            if board[j][i] != 0:
                colHeights.append(20-j)
                break
            elif j == 19:
                if board[j][i] != 0:
                    colHeights.append(1)
                else:
                    colHeights.append(0)

    columns = []
    for i in range(10):
        columns.append([row[i] for row in board])

    varA = aggregate(board, columns)
    varB = clearedLines(board) 
    varC = holes(board, columns)
    varD = bumpiness(board, columns, colHeights)
    varE = blockade(board, columns, colHeights)
    varF = tetrisSlot(board, columns[0])
    varG = iDependency(board, columns[1:], colHeights)

    return a*varA + b*varB + c*varC + d*varD + e*varE + f*varF + g*varG