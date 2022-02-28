from typing import List

import pygame
from pygame_widgets import WidgetHandler
from pygame_widgets.button import Button

from constants import PUZZLES_PER_PAGE, PUZZLES_PER_ROW, PUZZLES_PER_COLUMN, PUZZLE_SELECTION_EVENT, COLORS
from puzzles import puzzles


class PuzzleSelectionGraphic:
    def __init__(self, screen):
        self.mid_background_rect = None
        self.puzzle_idx = 0
        self.page_puzzles = []
        self.puzzle_selection_buttons: List[Button] = []
        self.mid_background_color = COLORS["ORANGE"]

        screen_width, screen_height = pygame.display.get_window_size()

        # puzzle selection background
        # leave 1/10th padding on all sides
        mid_background_padding_x = screen_width * 1 // 10
        mid_background_padding_y = screen_height * 1 // 10
        mid_background_width = screen_width * 4 // 5
        mid_background_height = screen_height * 4 // 5
        self.mid_background_rect = pygame.Rect(mid_background_padding_x, mid_background_padding_y,
                                               mid_background_width, mid_background_height)

        # draw a button for each puzzle on this page
        # padding measured from inside mid_background
        self.get_page_puzzles(screen)

    def clear_widgets(self):
        widgets = WidgetHandler.getWidgets()
        for btn in self.puzzle_selection_buttons:
            widgets.remove(btn)

    def get_page_puzzles(self, screen):
        puzzle_btn_padding_x = self.mid_background_rect.width * 1 // 16
        puzzle_btn_padding_y = self.mid_background_rect.height * 1 // 16
        puzzle_btn_width = self.mid_background_rect.width * 1 // 8
        puzzle_btn_height = self.mid_background_rect.height * 1 // 8

        self.page_puzzles = list(filter(
            lambda puzzle_node: self.puzzle_idx <= puzzle_node.num_id < (self.puzzle_idx + PUZZLES_PER_PAGE),
            puzzles.PUZZLES
        ))

        for i in range(PUZZLES_PER_ROW):
            puzzle_btn_offset_y = self.mid_background_rect.y + \
                                  i * (puzzle_btn_height + 2 * puzzle_btn_padding_y) + \
                                  puzzle_btn_padding_y
            for j in range(PUZZLES_PER_COLUMN):
                puzzle_btn_offset_x = self.mid_background_rect.x + \
                                      j * (puzzle_btn_width + 2 * puzzle_btn_padding_x) + \
                                      puzzle_btn_padding_x

                idx = i * PUZZLES_PER_ROW + j
                if idx < len(self.page_puzzles):
                    puzzle_btn = Button(
                        screen, puzzle_btn_offset_x, puzzle_btn_offset_y, puzzle_btn_width, puzzle_btn_height,
                        text="Puzzle - " + str(idx),
                        radius=10,
                        onClick=lambda p_id: pygame.event.post(
                            pygame.event.Event(PUZZLE_SELECTION_EVENT, {"puzzle_id": p_id}
                                               )),
                        onClickParams={self.page_puzzles[idx].num_id}
                    )
                    self.puzzle_selection_buttons.append(puzzle_btn)


