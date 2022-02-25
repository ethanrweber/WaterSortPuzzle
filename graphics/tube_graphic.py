from typing import List

import pygame as pg

from data.tube import Tube


class TubeGraphic:
    def __init__(self, tube: Tube, tube_x, tube_y, tube_graphic_width, tube_graphic_height, tube_border_width,
                 visual_indicator_offset: int):
        self.tube = tube
        self.tube_graphic = pg.Rect(tube_x, tube_y, tube_graphic_width, tube_graphic_height)
        self.tube_graphic_top_cover = pg.Rect(tube_x, tube_y, tube_graphic_width, tube_border_width)
        self.visual_indicator_offset = visual_indicator_offset

        self.tube_x = tube_x
        self.tube_y = tube_y
        self.tube_graphic_width = tube_graphic_width
        self.tube_graphic_height = tube_graphic_height
        self.tube_border_width = tube_border_width

        self.color_graphics: List[pg.Rect] = self.get_color_graphics(tube_x, tube_y,
                                                                     tube_graphic_width, tube_graphic_height,
                                                                     tube_border_width)
        self.is_selected = False

    def recreate_color_graphics(self):
        self.color_graphics = self.get_color_graphics(self.tube_x, self.tube_y,
                                                      self.tube_graphic_width, self.tube_graphic_height,
                                                      self.tube_border_width)

    def get_color_graphics(self, tube_x, tube_y, tube_graphic_width, tube_graphic_height, tube_border_width):
        # draw the liquids at each quarter of the tube from top to bottom
        # each tube has 4 liquid units,
        #   but they're drawn as 1/5th of the tube so the liquid doesn't appear to be overflowing
        color_graphics = []
        color_height_step = tube_graphic_height // 5
        # start the first color indented into the tube
        color_height = color_height_step
        for color_idx, color in enumerate(self.tube.data):

            drawing_last_color = color_idx == len(self.tube.data) - 1

            # make sure that the color fits inside the curved bottom of the tube
            current_color_height = color_height
            if drawing_last_color:
                current_color_height -= tube_border_width

            color_rect = pg.Rect(tube_x + tube_border_width, tube_y + current_color_height,
                                 tube_graphic_width - 2 * tube_border_width, color_height_step)

            color_graphics.append(color_rect)

            # increment the height at which the next section of liquid will be drawn
            color_height += color_height_step
        return color_graphics

    def __move_visual_indicator(self, offset):
        self.tube_graphic.update(self.tube_graphic.left,
                                 self.tube_graphic.top - offset,
                                 self.tube_graphic.width,
                                 self.tube_graphic.height)
        self.tube_graphic_top_cover.update(self.tube_graphic_top_cover.left,
                                           self.tube_graphic_top_cover.top - offset,
                                           self.tube_graphic_top_cover.width,
                                           self.tube_graphic_top_cover.height)
        for cg in self.color_graphics:
            cg.update(cg.left, cg.top - offset, cg.width, cg.height)

    def raise_visual_indicator(self):
        if not self.is_selected:
            self.is_selected = True
            self.__move_visual_indicator(self.visual_indicator_offset)

    def lower_visual_indicator(self):
        if self.is_selected:
            self.is_selected = False
            self.__move_visual_indicator(self.visual_indicator_offset * -1)
