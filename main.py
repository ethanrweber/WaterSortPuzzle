from constants import TUBE_HEIGHT, EMPTY_SYMBOL
from graph import Node, Graph
from tube import Tube


def receive_input():
    print("Enter the total number of tubes:")
    tube_count = int(input())
    print("Enter the number of empty tubes:")
    empty_tube_count = int(input())

    non_empty_tube_count = tube_count - empty_tube_count

    # make an array of tubes filled with the user-inputted number of empty tubes
    tubes = [Tube([EMPTY_SYMBOL] * TUBE_HEIGHT)] * empty_tube_count

    print("enter each color in the tube from top to bottom, accounting for each quarter of the tube length, separated by spaces.")
    print("for example, a tube might be half blue at the top and half red at the bottom, so enter \"blue blue red red\"")
    for i in range(non_empty_tube_count):
        print(f'Tube {i} of {non_empty_tube_count} (non empty tubes):')
        input_data = input().split()

        # account for missing symbols (assuming they're empty) -> prepend input data with empty symbols
        length = len(input_data)
        if length < TUBE_HEIGHT:
            input_data = [EMPTY_SYMBOL] * (TUBE_HEIGHT - length) + input_data

        tube = Tube(input_data)
        tubes.append(tube)

    node = Node(tubes, tube_count, empty_tube_count)
    return Graph(node)


if __name__ == '__main__':
    puzzle_graph = receive_input()

    print('data inputted:')
    print(puzzle_graph.start_node)

    print('is puzzle solvable?:')
    print(puzzle_graph.is_solvable(puzzle_graph.start_node))

    print('solved state:')
    print(puzzle_graph.final_node)
