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

MOVE_DELAY = 0.01

weights = [
    -1.530213,   # aggregate
     0.760667,   # increase tetris score after mvp
    -0.420690,   # bumpiness
    -5.474278,  # blockade
    -2.042069,   # tetris well
    -0.420420    # i piece dependencies
]


#6350k, 80% dimmer, current piece
pieceRGB = {
                "s":(86,234,80),  #green
                "z":(255,83,115), #red
                "j":(0,115,230),  #blue
                "l":(255,167,26), #orange
                "o":(255,255,56), #yellow
                "t":(187,51,203), #purple
                "i":(64,221,255) #light blue
            }

nextPieceRGB = {
                    "s":(81,184,77),  #green
                    "z":(235,79,101), #red
                    "j":(17,101,181), #blue
                    "l":(243,137,39), #orange
                    "o":(246,208,60), #yellow
                    "t":(151,57,162), #purple
                    "i":(66,175,225) #light blue
                }

boardRGB = {
                "s":[(81,184,77), (86,234,80)],  
                "z":[(235,79,101),(255,83,115)], 
                "j":[(17,101,181),(0,115,230)], 
                "l":[(243,137,39),(255,167,26)], 
                "o":[(246,208,60),(255,255,56)], 
                "t":[(151,57,162),(187,51,203)], 
                "i":[(66,175,225),(64,221,255)], 

                "x":(134,134,134),
                0:(0,0,0)
            }

pieces = {
            'z':[[['z', 'z', 0], [0, 'z', 'z']], [[0, 0, 'z'], [0, 'z', 'z'], [0, 'z', 0]]],
            's':[[[0, 's', 's'], ['s', 's', 0]], [['s', 0, 0], ['s', 's', 0], [0, 's', 0]]],
            'j':[[['j', 0, 0], ['j', 'j', 'j']], [['j', 'j'], ['j', 0], ['j', 0]], [['j', 'j', 'j'], [0, 0, 'j']], [[0, 'j'], [0, 'j'], ['j', 'j']]],
            'l':[[[0, 0, 'l'], ['l', 'l', 'l']], [['l', 0], ['l', 0], ['l', 'l']], [['l', 'l', 'l'], ['l', 0, 0]], [['l', 'l'], [0, 'l'], [0, 'l']]],
            'i':[[['i', 'i', 'i', 'i']], [['i'], ['i'], ['i'], ['i']]],
            't':[[[0, 't', 0], ['t', 't', 't']], [['t', 0], ['t', 't'], ['t', 0]], [['t', 't', 't'], [0, 't', 0]], [[0, 't'], ['t', 't'], [0, 't']]],
            'o':[[['o', 'o'], ['o', 'o']]],
            None:None 
        }


