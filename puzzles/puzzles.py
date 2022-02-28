from data.node import Node
from data.tube import Tube


# puzzles
def get_puzzle(puzzle_id: int):
    for puzzle in PUZZLES:
        if puzzle.num_id == puzzle_id:
            return puzzle
    return None


puzzle_id = 0


def add_puzzle(puz: Node):
    global puzzle_id
    puz.num_id = puzzle_id
    PUZZLES.append(puz)
    puzzle_id += 1

PUZZLES = []

# 1 - 10
add_puzzle(Node([
        Tube(['ORANGE', 'ORANGE']),
        Tube(['ORANGE', 'ORANGE'])
    ], 2, 2))

add_puzzle(Node([
        Tube(['ORANGE', 'ORANGE', 'BROWN', 'RED']),
        Tube(['BEIGE', 'MINT_GREEN', 'MINT_GREEN', 'BROWN']),
        Tube(['ORANGE', 'RED', 'MINT_GREEN', 'MINT_GREEN']),
        Tube(['BEIGE', 'RED', 'RED', 'BEIGE']),
        Tube(['BROWN', 'ORANGE', 'BEIGE', 'BROWN']),
        Tube([]),
        Tube([])
    ], 7, 2))

# todo: move this puzzle to like 50 when more get added
add_puzzle(Node([
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
    ], 14, 2))
