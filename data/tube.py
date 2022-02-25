from __future__ import annotations
from typing import List
from constants import TUBE_HEIGHT, EMPTY_SYMBOL


class Tube:
    def __init__(self, tube_array: List[str]):
        if len(tube_array) > TUBE_HEIGHT:
            raise Exception(f"tube length must not be greater than {TUBE_HEIGHT}:", tube_array)
        if len(tube_array) < TUBE_HEIGHT:
            tube_array = [EMPTY_SYMBOL] * (TUBE_HEIGHT - len(tube_array)) + tube_array
        self.data = tube_array

    def __str__(self):
        return ''.join(self.data) + 'T'

    def __eq__(self, other):
        return self.data == other.data

    def is_solved(self):
        colors = set(self.data)
        return self.data.count(self.data[0]) == TUBE_HEIGHT or len(colors) == 0

    def is_empty(self):
        return all(x == EMPTY_SYMBOL for x in self.data)

    # return the liquid at the top of the tube and how many units it takes up
    def top(self):
        """
        determine the liquid at the top of this Tube
        :return: (the liquid at the top of this Tube, the height of this liquid, the 0-based base-level of this liquid)
        """
        # find the first non-empty unit in the tube
        first_color = ''
        first_color_index = -1
        for i, color in enumerate(self.data):
            if color != EMPTY_SYMBOL:
                first_color_index, first_color = i, color
                break

        # if no non-empty unit was found, this tube is empty
        if first_color_index == -1:
            return EMPTY_SYMBOL, 0, TUBE_HEIGHT - 1

        # a non-empty unit was found, this tube is non-empty:
        # determine how tall the color is
        color_height = 1
        color_base = first_color_index
        for i, color in enumerate(self.data[first_color_index+1:], start=first_color_index+1):
            if color == EMPTY_SYMBOL:
                continue
            elif color == first_color:
                color_height += 1
                color_base = i
            # if the color "runs out", break out of the loop
            else:
                break

        return first_color, color_height, color_base

    def can_move_liquid_into(self, other: Tube) -> bool:
        """
        determine if liquid can be moved from Tube self to Tube other
        making a move:
            - liquid cannot be moved into nor out of a filled tube
            - liquid can be moved from one tube to another tube
                if the liquid at the top of both of tubes is the same type
            - when performing a move, as much of the liquid of the same type at the top of the tube is
                transferred to the other tube, as long as the target tube has the capacity to hold the liquid
        :param other: the target Tube
        :return: true if the top liquid in self can be transferred to Tube other, else false
        """
        self_color, self_height, self_color_base = self.top()
        other_color, other_height, other_color_base = other.top()

        # can't transfer out of self if self is empty
        if self_color == EMPTY_SYMBOL:
            return False

        # can always transfer into other if other is empty
        if other_color == EMPTY_SYMBOL:
            return True

        # both are non-empty:
        # liquid can be transferred if they share the same top color AND if the target tube has at least one capacity
        return self_color == other_color and (other_color_base + 1 - other_height) > 0

    def move_liquid(self, other: Tube):
        """
        moves liquid from Tube self to Tube other while it can move that liquid.
        does nothing if a liquid cannot be moved
        :param other: the target Tube
        :return: nothing
        """
        while self.can_move_liquid_into(other):
            self_color, self_height, self_color_base = self.top()
            other_color, other_height, other_color_base = other.top()

            self.data[self_color_base + 1 - self_height] = EMPTY_SYMBOL
            # set top value of 'other' to self_color - can't use other_color because other_color might be EMPTY_SYMBOL
            other.data[other_color_base - other_height] = self_color
