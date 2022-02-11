from typing import List
from tube import Tube
from constants import TUBE_HEIGHT, EMPTY_SYMBOL


class Node:
    def __init__(self, tube_array: List[Tube], tube_count, empty_tube_count):
        self.data = tube_array
        self.tube_count = tube_count
        self.empty_tube_count = empty_tube_count

        if not self.is_valid():
            raise Exception("Invalid Puzzle")

    def __str__(self):
        if len(self.data) == 0:
            return ''
        return 'T'.join(sorted(str(tube) for tube in self.data)) + 'T' # T to delimit tubes

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

    def solve(self):
        # solve the puzzle (?):
        # turn tubes matrix into graph representation
        #   turn each tube into a standard string representation
        #   put the strings in order and concatenate them

        # making a move:
        # liquid cannot be moved into nor out of a filled tube
        # liquid can be moved from one tube to another tube if the liquid at the top of both of tubes is the same type
        #   when performing a move, as much of the liquid of the same type at the top of the tube is
        #   transferred to the other tube, as long as the target tube has the capacity to hold the liquid

        if not self.is_solved():
            pass

        return


class Graph:
    def __init__(self, start_node: Node):
        self.start_node = start_node
        self.tube_count = start_node.tube_count

        self.final_node = self.generate_final_state()

    def generate_final_state(self):
        # build the final state of the graph from the start state
        colors = set()
        for tube in self.start_node.data:
            for color in tube.data:
                colors.add(color)
        colors -= set(EMPTY_SYMBOL)  # exclude the empty symbol from consideration

        number_empty_tubes = self.tube_count - len(colors)

        final_tubes = [Tube([EMPTY_SYMBOL] * TUBE_HEIGHT)] * number_empty_tubes
        for color in colors:
            final_tube = Tube([color] * TUBE_HEIGHT)
            final_tubes.append(final_tube)

        return Node(final_tubes, self.tube_count, number_empty_tubes)



