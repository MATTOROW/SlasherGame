WIDTH = 1280
HEIGHT = 704
FPS = 60
TILESIZE = 64

LEVEL_MAP = [
    ' x xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    ' xp                                       x',
    ' x                                        x',
    ' xxxxxxxxx                                x',
    ' xxxxxxxxxxx                              x',
    ' xxxxxxxxxxxxxxx     x                    x',
    ' xxxxxxxxxxxxxxx     x                    x',
    ' xxxxxxxxxxxxxxx     x                    x',
    ' xxxxxxxxxxxxxxx     x                    x',
    ' xxxxxxxxxxxxxxxxxxxxxxxxx                x',
    ' xxxxxxxxxxxxxxxxxxxxxxxxxxxx            xx',
    ' xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    '                                           ',
    '                                           ',
    '                                           ',
    '                                           ',
    '                                           ',
    '                                           ',
    '                                           ',
    '                                           ',
    '                                           ',
    '                                           ',
    '                                           ',
    ' xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
]

LEVEL_WIDTH = len(LEVEL_MAP[0]) * TILESIZE
LEVEL_HEIGHT = len(LEVEL_MAP) * TILESIZE