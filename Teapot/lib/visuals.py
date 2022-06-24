class colors:
    lime = '\x1b[38;2;86;234;80m'
    red = '\x1b[38;2;255;83;115m'
    lblue = '\x1b[38;2;64;221;255m'
    magenta = '\x1b[38;2;187;51;203m'
    yellow = '\x1b[38;2;255;255;56m'
    blue = '\x1b[38;2;0;115;230m'
    orange = '\x1b[38;2;255;167;26m'
    garbage = '\x1b[38;2;134;134;134m'
    reset = "\u001b[37m"

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
        case 'x':
            return colors.garbage
        case _:
            return colors.reset

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
            print(getColor(tile) + str(tile) + " " + colors.reset, end="")
        print("\r")

        n += 1
