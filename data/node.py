from typing import List

from constants import EMPTY_SYMBOL, TUBE_HEIGHT
from data.tube import Tube


class Node:
    def __init__(self, tube_array: List[Tube], tube_count, empty_tube_count):
        self.data = tube_array
        self.tube_count = tube_count
        self.empty_tube_count = empty_tube_count
        self.move_list = []
        # self.description_of_moves = ""

        if not self.is_valid():
            raise Exception("Invalid Puzzle")

    def __str__(self):
        if len(self.data) == 0:
            return ''
        return ''.join(sorted(str(tube) for tube in self.data))

    def __eq__(self, other):
        # Node other may have Tubes swapped but with the same values, so string comparison is the most straightforward
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))

    def description_of_moves(self):
        return '\n'.join(f"Moved liquid from Tube {i + 1} to Tube {j + 1}" for (i, j) in self.move_list)

    def is_valid(self):
        # a puzzle is valid iff each color type appears in exactly 4 quarters total out of all tubes
        colors = dict()
        for tube in self.data:
            for color in tube.data:
                if color == EMPTY_SYMBOL:
                    continue

                if color in colors:
                    colors[color] += 1
                else:
                    colors[color] = 1

        for color in colors:
            if colors[color] != TUBE_HEIGHT:
                return False
        return True

    def is_solved(self):
        # conditions for a solved puzzle:
        # any single tube in the puzzle is either empty or filled completely with only one liquid type
        return all(map(lambda tube: tube.is_solved(), self.data))
