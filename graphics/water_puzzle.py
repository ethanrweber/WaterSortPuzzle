from typing import List

import pygame as pg

from constants import FPS, COLORS, EMPTY_SYMBOL
from data.node import Node
from data.tube import Tube
from graphics.tube_graphic import TubeGraphic

pg.display.set_caption("Water Sorting Puzzle")
WIDTH, HEIGHT = WINDOW_SIZE = (900, 600)
window = pg.display.set_mode(WINDOW_SIZE, pg.RESIZABLE)

BACKGROUND_COLOR = COLORS["GRAY"]
COLORS[EMPTY_SYMBOL] = BACKGROUND_COLOR

TUBE_GRAPHIC_WIDTH, TUBE_GRAPHIC_HEIGHT = WIDTH // 10, HEIGHT // 2
TUBE_BORDER_WIDTH = 5
TUBE_BORDER_RADIUS = TUBE_GRAPHIC_WIDTH // 2
TUBE_VISUAL_INDICATOR_OFFSET = 20

# todo: make this selectable on another screen from a list of puzzles
GAME_PUZZLE = Node([
    Tube(['BLUE', 'BLUE', 'ORANGE', 'MINT_GREEN']),
    Tube(['ORANGE', 'ORANGE', 'BLUE', 'ORANGE']),
    Tube(['MINT_GREEN', 'MINT_GREEN', 'MINT_GREEN', 'BLUE']),
    Tube([]),
    Tube([])
], 5, 2)

n = len(GAME_PUZZLE.data)
remaining_space = WIDTH - (n * TUBE_GRAPHIC_WIDTH)
space_between_tubes = remaining_space // (n + 1)


def draw_tube_colors(tube, tube_x, tube_y, can_raise_tube_visual_indicator):
    # draw the liquids at each quarter of the tube from top to bottom
    color_height_step = TUBE_GRAPHIC_HEIGHT // 5
    # start the first color indented into the tube so the liquid doesn't appear to be overflowing
    color_height = color_height_step
    for color_idx, color in enumerate(tube.data):
        # draw the color inside the tube's borders
        drawing_last_color = color_idx == len(tube.data) - 1
        # make sure that the color fits inside the curved bottom of the tube
        current_color_height = color_height
        if drawing_last_color:
            current_color_height -= TUBE_BORDER_WIDTH

        if can_raise_tube_visual_indicator:
            color_rect = pg.Rect(tube_x + TUBE_BORDER_WIDTH,
                                 tube_y + current_color_height - TUBE_VISUAL_INDICATOR_OFFSET,
                                 TUBE_GRAPHIC_WIDTH - 2 * TUBE_BORDER_WIDTH, color_height_step)
        else:
            color_rect = pg.Rect(tube_x + TUBE_BORDER_WIDTH,
                                 tube_y + current_color_height,
                                 TUBE_GRAPHIC_WIDTH - 2 * TUBE_BORDER_WIDTH, color_height_step)

        # draw the section of liquid
        if drawing_last_color:
            pg.draw.rect(window, COLORS[color], color_rect,
                         border_bottom_left_radius=TUBE_BORDER_RADIUS,
                         border_bottom_right_radius=TUBE_BORDER_RADIUS)
        else:
            pg.draw.rect(window, COLORS[color], color_rect)

        # increment the height at which the next section of liquid will be drawn
        color_height += color_height_step


def draw_tubes(puzzle: Node):
    # draw the tubes in start node
    tube_x = 0
    tube_y = HEIGHT // 4
    # draw each tube
    for tube_idx, tube in enumerate(puzzle.data):
        tube_x += space_between_tubes

        tube_graphic = TubeGraphic(
            tube=tube,
            tube_graphic=pg.Rect(tube_x, tube_y, TUBE_GRAPHIC_WIDTH, TUBE_GRAPHIC_HEIGHT),
            tube_graphic_top_cover=pg.Rect(tube_x, tube_y, TUBE_GRAPHIC_WIDTH, TUBE_BORDER_WIDTH),
            visual_indicator_offset=TUBE_VISUAL_INDICATOR_OFFSET
        )

        # check if current graphic is selected. if so, raise it slightly as a visual indicator
        mouse_clicked = pg.mouse.get_pressed()[0]
        mouse_tube_collision = tube_graphic.tube_graphic.collidepoint(pg.mouse.get_pos())
        tube_empty = tube.is_empty()
        can_raise_tube_visual_indicator = mouse_clicked and mouse_tube_collision and not tube_empty

        if can_raise_tube_visual_indicator:
            tube_graphic.raise_visual_indicator()

        # draw the tube outline
        pg.draw.rect(window, COLORS["BLACK"], tube_graphic.tube_graphic, width=TUBE_BORDER_WIDTH,
                     border_bottom_left_radius=TUBE_BORDER_RADIUS, border_bottom_right_radius=TUBE_BORDER_RADIUS)

        # hide the top border of the tube, so it appears open
        pg.draw.rect(window, BACKGROUND_COLOR, tube_graphic.tube_graphic_top_cover)

        # draw the colors inside the tube
        draw_tube_colors(tube, tube_x, tube_y, can_raise_tube_visual_indicator)

        # increment the x position at which the next tube will be drawn
        tube_x += TUBE_GRAPHIC_WIDTH


def draw_window(game_puzzle):
    # set background color
    window.fill(BACKGROUND_COLOR)

    draw_tubes(game_puzzle)

    pg.display.update()


def main():
    # game setup
    clock = pg.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        draw_window(GAME_PUZZLE)


if __name__ == '__main__':
    main()
    pg.quit()
