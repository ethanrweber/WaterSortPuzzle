from typing import List

import pygame as pg

from data.tube import Tube


class TubeGraphic:
    def __init__(self, tube: Tube, tube_graphic: pg.Rect, tube_graphic_top_cover: pg.Rect,
                 visual_indicator_offset: int):
        self.tube = tube
        self.tube_graphic = tube_graphic
        self.tube_graphic_top_cover = tube_graphic_top_cover
        self.visual_indicator_offset = visual_indicator_offset

    def raise_visual_indicator(self):
        self.tube_graphic.update(self.tube_graphic.left, self.tube_graphic.top - self.visual_indicator_offset,
                                 self.tube_graphic.width, self.tube_graphic.height)
        self.tube_graphic_top_cover.update(self.tube_graphic_top_cover.left,
                                           self.tube_graphic_top_cover.top - self.visual_indicator_offset,
                                           self.tube_graphic_top_cover.width,
                                           self.tube_graphic_top_cover.height)
