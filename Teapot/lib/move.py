import keyboard
import time


def rotationOffset(piece, dir):
    match piece:
        case 's':
            match dir:
                case 1:
                    return 1
                case 0:
                    return 0
        case 'z':
            match dir:
                case 1:
                    return 0
                case 0:
                    return 0
        case 'l':
            match dir:
                case 1:
                    return 1
                case _:
                    return 0 
        case 'j':
            match dir:
                case 1:
                    return 1
                case _:
                    return 0
        case 'i':
            match dir:
                case 1:
                    return 2
                case 3:
                    return 1
                case _:
                    return 0
        case 't':
            match dir:
                case 1:
                    return 1
                case _:
                    return 0
        case 'o':
            return 1



def place(dir, pos, piece):
    #!ROTATION!#
    #0:no rotat, 1:cw rotat, 2: 180 rotat, 3: ccw rotat
    rotationModifier = rotationOffset(piece, dir)
    if dir == 1:
        keyboard.press_and_release('x')
    elif dir == 3:
        keyboard.press_and_release('z')
    elif dir == 2:
        keyboard.press_and_release('a')


    #!MOVEMENT!#
    #pieces leftmost edge will always be at index 3, except o piece at 4, z piece has empty corner there
    movement = -(3 - pos + rotationModifier)
    for i in range(abs(movement)):
        if movement < 0:
            keyboard.press_and_release('left')
        else:
            keyboard.press_and_release('right')



    #!DROP!#
    time.sleep(0.03)
    keyboard.press_and_release('space')

def hold():
    time.sleep(0.01)
    keyboard.press_and_release('c')
