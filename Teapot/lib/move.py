import time
import ctypes
import random
from . constants import MOVE_DELAY

lookup = {
    'a': 0x41,  # VK_A
    'z': 0x5A,  # VK_Z
    'x': 0x58,  # VK_X
    'left': 0x25,  # VK_LEFT
    'right': 0x27,  # VK_RIGHT
    'space': 0x20,  # VK_SPACE
    'c': 0x43,  # VK_C
    'r': 0x52   # VK_R
}

def press_and_release(key):
    KEY_CODE = lookup[key]
    ctypes.windll.user32.keybd_event(KEY_CODE, 0, 0, 0)
    ctypes.windll.user32.keybd_event(KEY_CODE, 0, 2, 0)


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
        press_and_release('x')
    elif dir == 3:
        press_and_release('z')
    elif dir == 2:
        press_and_release('a')

    time.sleep(0.01)

    #!MOVEMENT!#
    #pieces leftmost edge will always be at index 3, except o piece at 4, z piece has empty corner there
    movement = -(3 - pos + rotationModifier)
    for i in range(abs(movement)):
        time.sleep(random.uniform(0.01, MOVE_DELAY))
        if movement < 0:
            press_and_release('left')
        else:
            press_and_release('right')


    time.sleep(random.uniform(0.01, MOVE_DELAY))
    #!DROP!#
    press_and_release('space')
    

def hold():
    time.sleep(MOVE_DELAY)
    press_and_release('c')


def retry():
    ctypes.windll.user32.keybd_event(lookup['r'], 0, 0, 0)
    time.sleep(1)
    ctypes.windll.user32.keybd_event(lookup['r'], 0, 2, 0)