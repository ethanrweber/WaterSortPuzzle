from typing import List
from tube import Tube
from constants import TUBE_HEIGHT, EMPTY_SYMBOL
from copy import deepcopy


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
        return ''.join(sorted(str(tube) for tube in self.data))

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


class Graph:
    def __init__(self, start_node: Node):
        self.start_node = start_node
        # all nodes should have the same number of tubes
        self.tube_count = start_node.tube_count

        self.final_node = self.generate_final_state()

        self.vertices = [self.start_node, self.final_node]

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

    def is_solvable(self, start_node: Node):
        # solve the puzzle (?):

        # base case: if puzzle is solved, stop
        if start_node.is_solved():
            return True

        # iterate through all possible moves
        result = False
        for i, tube_one in enumerate(start_node.data):
            if result:
                break
            for j, tube_two in enumerate(start_node.data, start=(i+1)):
                # check if liquid can be moved from tube one to tube two OR vice versa
                if tube_one.can_move_liquid_into(tube_two):
                    # deepcopy node
                    copy_node = deepcopy(start_node)
                    # move liquid in copied node
                    copy_node.data[i].move_liquid(copy_node.data[j])
                    # recurse solve
                    result = result or self.is_solvable(copy_node)
                    if result:
                        break
                if tube_two.can_move_liquid_into(tube_one):
                    # deepcopy node
                    copy_node = deepcopy(start_node)
                    # move liquid in copied node
                    copy_node.data[j].move_liquid(copy_node.data[i])
                    # recurse solve
                    result = result or self.is_solvable(copy_node)
                    if result:
                        break

        return result

