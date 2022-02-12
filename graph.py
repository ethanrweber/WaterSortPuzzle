from functools import cache
from typing import List

from Node import Node
from tube import Tube
from constants import TUBE_HEIGHT, EMPTY_SYMBOL
from copy import deepcopy


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

    def solve(self, start_node: Node, path: List[Node]) -> (bool, Node):
        """
        solves the puzzle
        :param start_node:
        :param path:
        :return: (boolean: was the puzzle solved?, path: the list of nodes iterated through to solve the puzzle)
        """

        # base case: if puzzle is solved, stop
        if start_node.is_solved():
            return True, path[-1]

        # detect loops: if current node has already been detected, stop recursing
        if start_node in path and path.index(start_node) != len(path) - 1:
            return False, path[-1]

        # iterate through all possible moves
        for i, tube_one in enumerate(start_node.data):
            for j, tube_two in enumerate(start_node.data[i+1:], start=(i+1)):
                # check if liquid can be moved from tube one to tube two OR vice versa
                if tube_one.can_move_liquid_into(tube_two):
                    # deepcopy node
                    copy_node = deepcopy(start_node)
                    # move liquid in copied node and update path description
                    copy_node.description_of_moves += f"Moved liquid from Tube {i + 1} ({tube_one}) to Tube {j + 1} ({tube_two})\n"
                    copy_node.data[i].move_liquid(copy_node.data[j])
                    # recurse solve
                    result, final_node = self.solve(copy_node, path + [copy_node])
                    if result:
                        return True, final_node
                if tube_two.can_move_liquid_into(tube_one):
                    # deepcopy node
                    copy_node = deepcopy(start_node)
                    # move liquid in copied node
                    copy_node.description_of_moves += f"Moved liquid from Tube {j + 1} ({tube_two}) to Tube {i + 1} ({tube_one})\n"
                    copy_node.data[j].move_liquid(copy_node.data[i])
                    # recurse solve
                    result, final_node = self.solve(copy_node, path + [copy_node])
                    if result:
                        return True, final_node

        return False, path[-1]

