import unittest

from graph import Graph, Node
from tube import Tube

PRINT_DESCRIPTIONS = True

o = 'orange '
b = 'blue '
m = 'mint_green '
r = 'brown '
e = 'red '
s = 'beige '
y = 'yellow '
g = 'green '
p = 'pink '
c = 'cyan '
u = 'purple '

class TestGraphMethods(unittest.TestCase):
    # Test Graph.solve()
    # test cases for Graph.solve() based off of levels from the game
    def test_case_one(self):
        puzzle = Graph(Node([
            Tube([o, o]),
            Tube([o, o])
        ], 2, 0))

        expected_result = Node([
            Tube([o, o, o, o]),
            Tube([])
        ], 2, 1)

        solved, result_node = puzzle.solve(puzzle.start_node, [])
        self.assertTrue(solved)
        self.assertEqual(expected_result, result_node)
        if PRINT_DESCRIPTIONS:
            print('test case one:')
            print(result_node.description_of_moves)

    def test_case_two(self):
        puzzle = Graph(Node([
            Tube([o, o]),
            Tube([b, b, b]),
            Tube([b, o, o])
        ], 3, 0))

        expected_result = Node([
            Tube([]),
            Tube([b, b, b, b]),
            Tube([o, o, o, o])
        ], 3, 1)

        solved, result_node = puzzle.solve(puzzle.start_node, [])
        self.assertTrue(solved)
        self.assertEqual(expected_result, result_node)
        if PRINT_DESCRIPTIONS:
            print('test case two:')
            print(result_node.description_of_moves)

    def test_case_three(self):
        puzzle = Graph(Node([
            Tube([b, b, o, m]),
            Tube([o, o, b, o]),
            Tube([m, m, m, b]),
            Tube([]),
            Tube([])
        ], 5, 2))

        expected_result = Node([
            Tube([]),
            Tube([]),
            Tube([b, b, b, b]),
            Tube([o, o, o, o]),
            Tube([m, m, m, m])
        ], 5, 2)

        solved, result_node = puzzle.solve(puzzle.start_node, [])
        self.assertTrue(solved)
        self.assertEqual(expected_result, result_node)
        if PRINT_DESCRIPTIONS:
            print('test case three:')
            print(result_node.description_of_moves)

    def test_case_four(self):
        puzzle = Graph(Node([
            Tube([o, r, o, r]),
            Tube([b, b, r, b]),
            Tube([r, o, o, b]),
            Tube([]),
            Tube([])
        ], 5, 2))

        expected_result = Node([
            Tube([]),
            Tube([]),
            Tube([b, b, b, b]),
            Tube([o, o, o, o]),
            Tube([r, r, r, r])
        ], 5, 2)

        solved, result_node = puzzle.solve(puzzle.start_node, [])
        self.assertTrue(solved)
        self.assertEqual(expected_result, result_node)
        if PRINT_DESCRIPTIONS:
            print('test case four:')
            print(result_node.description_of_moves)

    def test_case_five(self):
        puzzle = Graph(Node([
            Tube([o, o, r, e]),
            Tube([s, m, m, r]),
            Tube([o, e, m, m]),
            Tube([s, e, e, s]),
            Tube([r, o, s, r]),
            Tube([]),
            Tube([])
        ], 7, 2))

        expected_result = Node([
            Tube([]),
            Tube([]),
            Tube([s, s, s, s]),
            Tube([e, e, e, e]),
            Tube([m, m, m, m]),
            Tube([o, o, o, o]),
            Tube([r, r, r, r])
        ], 7, 2)

        solved, result_node = puzzle.solve(puzzle.start_node, [])
        self.assertTrue(solved)
        self.assertEqual(expected_result, result_node)
        if PRINT_DESCRIPTIONS:
            print('test case five:')
            print(result_node.description_of_moves)

    def test_case_one_hundred_twelve(self):
        puzzle = Graph(Node([
            Tube([y, b, p, y]),
            Tube([b, g, m, c]),
            Tube([y, u, c, o]),
            Tube([r, o, u, g]),
            Tube([c, e, g, b]),
            Tube([u, p, p, y]),
            Tube([e, r, r, e]),
            Tube([m, b, o, c]),
            Tube([m, u, e, m]),
            Tube([p, o, r, g]),
            Tube([]),
            Tube([])
        ], 12, 2))

        expected_result = Node([
            Tube([]),
            Tube([]),
            Tube([g, g, g, g]),
            Tube([c, c, c, c]),
            Tube([u, u, u, u]),
            Tube([p, p, p, p]),
            Tube([b, b, b, b]),
            Tube([y, y, y, y]),
            Tube([e, e, e, e]),
            Tube([m, m, m, m]),
            Tube([o, o, o, o]),
            Tube([r, r, r, r])
        ], 12, 2)

        solved, result_node = puzzle.solve(puzzle.start_node, [])
        self.assertTrue(solved)
        self.assertEqual(expected_result, result_node)
        if PRINT_DESCRIPTIONS:
            print('test case one hundred twelve:')
            print(result_node.description_of_moves)



if __name__ == '__main__':
    unittest.main()
