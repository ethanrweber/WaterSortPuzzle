from typing import List
from constants import TUBE_HEIGHT


class Tube:
    def __init__(self, tube_array: List[str]):
        if len(tube_array) > TUBE_HEIGHT:
            raise Exception(f"tube length must not be greater than {TUBE_HEIGHT}:", tube_array)
        self.data = tube_array

    def __str__(self):
        return ''.join(self.data)

    def is_solved(self):
        colors = set(self.data)
        return self.data.count(self.data[0]) == self.tube_height or len(colors) == 0
