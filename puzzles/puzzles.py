from data.node import Node
from data.tube import Tube

# todo: move from strings to ints?
# color encodings
# ORANGE = 0
# BROWN = 1
# RED = 2
# BEIGE = 3
# MINT_GREEN = 4
# BROWN = 5
# GRAY = 6
# YELLOW = 7
# PURPLE = 8
# GREEN = 9


# puzzles
puzzle_id = 0

puzzle_0 = Node([
    Tube(['ORANGE', 'ORANGE']),
    Tube(['ORANGE', 'ORANGE'])
], 2, 2, puzzle_id)

puzzle_id += 1

puzzle_1 = Node([
    Tube(['ORANGE', 'ORANGE', 'BROWN', 'RED']),
    Tube(['BEIGE', 'MINT_GREEN', 'MINT_GREEN', 'BROWN']),
    Tube(['ORANGE', 'RED', 'MINT_GREEN', 'MINT_GREEN']),
    Tube(['BEIGE', 'RED', 'RED', 'BEIGE']),
    Tube(['BROWN', 'ORANGE', 'BEIGE', 'BROWN']),
    Tube([]),
    Tube([])
], 7, 2, 1)

puzzle_id += 1

puzzle_100 = Node([
    Tube(['MINT_GREEN', 'GRAY', 'ORANGE', 'YELLOW']),
    Tube(['RED', 'PURPLE', 'GREEN', 'CYAN']),
    Tube(['GREEN', 'PINK', 'MINT_GREEN', 'PURPLE']),
    Tube(['YELLOW', 'PINK', 'RED', 'BROWN']),
    Tube(['GREEN', 'VIOLET', 'BROWN', 'PURPLE']),
    Tube(['GREEN', 'GRAY', 'PURPLE', 'YELLOW']),
    Tube(['ORANGE', 'GRAY', 'CYAN', 'DARK_GREEN']),
    Tube(['RED', 'DARK_GREEN', 'CYAN', 'PINK']),
    Tube(['VIOLET', 'VIOLET', 'CYAN', 'MINT_GREEN']),
    Tube(['DARK_GREEN', 'BROWN', 'PINK', 'ORANGE']),
    Tube(['GRAY', 'MINT_GREEN', 'YELLOW', 'ORANGE']),
    Tube(['RED', 'BROWN', 'DARK_GREEN', 'VIOLET']),
    Tube([]),
    Tube([])
], 14, 2)
