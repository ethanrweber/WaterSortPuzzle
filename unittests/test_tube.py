import unittest
from data.tube import Tube
from constants import EMPTY_SYMBOL

# Some test cases assume constants.TUBE_HEIGHT = 4
class TestTubeMethods(unittest.TestCase):
    # Test cases for Tube.is_solved()
    def test_full_tube_one_color_is_solved(self):
        tube = Tube(['blue'] * 4)
        self.assertTrue(tube.is_solved())

    def test_empty_tube_is_solved(self):
        tube = Tube([])
        self.assertTrue(tube.is_solved())

    def test_half_full_tube_one_color_is_not_solved(self):
        tube = Tube(['blue'] * 2)
        self.assertFalse(tube.is_solved())

    def test_full_tube_multiple_colors_is_not_solved(self):
        tube = Tube(['blue'] * 2 + ['yellow'] * 2)
        self.assertFalse(tube.is_solved())

    # Test cases for Tube.top()
    def test_top_of_tube_is_blue(self):
        tube = Tube(['blue'])
        color, color_height, color_base = tube.top()
        self.assertEqual(color, 'blue')

    def test_top_of_tube_at_bottom_of_array(self):
        tube = Tube(['blue'])
        color, color_height, color_base = tube.top()
        self.assertEqual(color_base, len(tube.data) - 1)

    def test_top_of_tube_color_height(self):
        expected_height = 3
        tube = Tube(['blue'] * expected_height)
        color, color_height, color_base = tube.top()
        self.assertEqual(color_height, expected_height)

    def test_top_of_empty_tube_is_empty_symbol(self):
        tube = Tube([])
        color, color_height, color_base = tube.top()
        self.assertEqual(color, EMPTY_SYMBOL)

    def test_top_of_empty_tube_has_zero_height(self):
        tube = Tube([])
        color, color_height, color_base = tube.top()
        self.assertEqual(color_height, 0)

    def test_top_of_empty_tube_base_at_bottom_of_tube(self):
        tube = Tube([])
        color, color_height, color_base = tube.top()
        self.assertEqual(color_base, len(tube.data) - 1)


    # Test cases for Tube.can_move_liquid_into()
    def test_can_move_liquid_from_tube_to_tube_of_equal_height(self):
        tube_a = Tube(['blue'] * 2)
        tube_b = Tube(['blue'] * 2)
        self.assertTrue(tube_a.can_move_liquid_into(tube_b))

    def test_can_move_liquid_from_filled_tube_to_half_filled_tube(self):
        tube_a = Tube(['blue'] * 4)
        tube_b = Tube(['blue'] * 2)
        self.assertTrue(tube_a.can_move_liquid_into(tube_b))

    def test_can_move_liquid_from_filled_tube_to_empty_tube(self):
        tube_a = Tube(['blue'] * 4)
        tube_b = Tube([])
        self.assertTrue(tube_a.can_move_liquid_into(tube_b))

    def test_cannot_move_liquid_from_empty_tube_to_empty_tube(self):
        tube_a = Tube([])
        tube_b = Tube([])
        self.assertFalse(tube_a.can_move_liquid_into(tube_b))

    def test_cannot_move_liquid_from_empty_tube_to_filled_tube(self):
        tube_a = Tube([])
        tube_b = Tube(['blue'] * 4)
        self.assertFalse(tube_a.can_move_liquid_into(tube_b))

    def test_cannot_move_liquids_of_different_types(self):
        tube_a = Tube(['yellow'] * 2)
        tube_b = Tube(['blue'] * 2)
        self.assertFalse(tube_a.can_move_liquid_into(tube_b))

    # Test cases for Tube.move_liquid
    def test_move_liquid_from_full_tube_to_empty_tube(self):
        expected_color = 'blue'
        tube_a = Tube([expected_color] * 4)
        tube_b = Tube([])
        tube_a.move_liquid(tube_b)

        assertion_a = all(x == EMPTY_SYMBOL for x in tube_a.data)
        assertion_b = all(y == expected_color for y in tube_b.data)
        self.assertTrue(assertion_a, msg='tube A is empty')
        self.assertTrue(assertion_b, msg=f'tube B is filled with \'{expected_color}\'')

    def test_move_liquid_from_half_full_tube_to_half_full_tube_of_same_color(self):
        expected_color = 'blue'
        tube_a = Tube([expected_color] * 2)
        tube_b = Tube([expected_color] * 2)
        tube_a.move_liquid(tube_b)

        assertion_a = all(x == EMPTY_SYMBOL for x in tube_a.data)
        assertion_b = all(y == expected_color for y in tube_b.data)
        self.assertTrue(assertion_a, msg='tube A is empty')
        self.assertTrue(assertion_b, msg=f'tube B is filled with \'{expected_color}\'')

    def test_move_liquid_cannot_move_different_liquids(self):
        tube_a = Tube(['blue'] * 2)
        tube_b = Tube(['yellow'] * 2)
        tube_a.move_liquid(tube_b)

        assertion_a = tube_a.data.count('blue') == 2
        assertion_b = tube_b.data.count('yellow') == 2
        self.assertTrue(assertion_a, msg='tube A should have the same liquids it started with')
        self.assertTrue(assertion_b, msg='tube B should have the same liquids it started with')

    def test_move_liquid_variety(self):
        tube_a = Tube(['red', 'yellow', 'blue', 'blue'])
        tube_b = Tube(['red', 'blue', 'blue'])
        tube_a.move_liquid(tube_b)

        expected_tube_a = Tube(['yellow', 'blue', 'blue'])
        expected_tube_b = Tube(['red', 'red', 'blue', 'blue'])
        self.assertEqual(tube_a, expected_tube_a)
        self.assertEqual(tube_b, expected_tube_b)

    def test_move_liquid_with_potential_overflow(self):
        tube_a = Tube(['red', 'red', 'red', 'blue'])
        tube_b = Tube(['red', 'blue'])
        tube_a.move_liquid(tube_b)

        expected_tube_a = Tube(['red', 'blue'])
        expected_tube_b = Tube(['red', 'red', 'red', 'blue'])
        self.assertEqual(tube_a, expected_tube_a)
        self.assertEqual(tube_b, expected_tube_b)


if __name__ == '__main__':
    unittest.main()
