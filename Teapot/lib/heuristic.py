def aggregate(board):
    aggregateHeight = 0
    for i in range(10):
        for j in range(20):
            if board[j][i] != 0:
                #find first non empty tile in the board and apply non-linear scaling
                aggregateHeight += (20 - j) ** 1.5
                break

    return aggregateHeight/10

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
            clearedLines *= 10 #tetris gucci af
        case 3:
            clearedLines *= 0.75 #triple are horrible value
        case 2:
            clearedLines *= 1.5 #doubles are ok
        case 1:
            clearedLines *= 1 #singles are ok cause im fast
            
    return clearedLines

def bumpiness(colHeights):
    bumpiness = 0

    prevH = colHeights[1]
    for h in range(2, len(colHeights)): #get difference between adjacent columns
        bumpiness += abs(prevH - colHeights[h])
        prevH = colHeights[h]
        
    return bumpiness

def blockade(columns):
    blockade = 0

    for i in range(10):
        isEmpty = False
        for j in range(19, -1, -1):
            if columns[i][j] == 0:
                isEmpty = True
            
            if isEmpty and columns[i][j] != 0: #this tile is blocking a empty space
                blockade += 1
   
    return blockade ** 0.75 #non-linear scaling

def tetrisSlot(board, well):
    blocking = 0
    for i in range(20):
        lineCleared = 0 not in board[i]
        if (well[i] != "i" and well[i] != 0) or well[i] == "i" and not lineCleared:
            blocking += 1

    return blocking

def iDependency(colHeights):
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


def analyze(board, weights):
    a, b, c, d, e, f = weights

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

    varA = aggregate(board)
    varB = clearedLines(board) 
    varC = bumpiness(colHeights)
    varD = blockade(columns)
    varE = tetrisSlot(board, columns[0])
    varF = iDependency(colHeights)

    return a*varA + b*varB + c*varC + d*varD + e*varE + f*varF
