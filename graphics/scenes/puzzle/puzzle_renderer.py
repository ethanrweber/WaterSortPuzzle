from typing import List

import pygame as pg

from constants import WIDTH, HEIGHT, TUBE_GRAPHIC_WIDTH, TUBE_GRAPHIC_HEIGHT, TUBE_BORDER_WIDTH, TUBE_BORDER_RADIUS, \
    TUBE_VISUAL_INDICATOR_OFFSET, UPDATE_TUBE_EVENT, COLORS, BACKGROUND_COLOR
from data.node import Node
from graphics.graphics_objects.tube_graphic import TubeGraphic


def create_tube_graphics(puzzle: Node) -> List[TubeGraphic]:
    # graphics setup
    n = len(puzzle.data)

    remaining_space = WIDTH - (n * TUBE_GRAPHIC_WIDTH)
    space_between_tubes = remaining_space // (n + 1)

    # draw the tubes in start node
    tube_graphics = []

    tube_x = space_between_tubes
    tube_y = HEIGHT // 8

    # determine whether to draw tubes all on one line or on multiple rows
    multiple_rows = len(puzzle.data) >= 10
    tube_row_delimiter = len(puzzle.data) // 2 - 1
    multiple_row_offset = WIDTH // 8 + space_between_tubes

    if multiple_rows:
        space_between_tubes *= 2
        tube_x = multiple_row_offset

    # draw each tube
    for tube_idx, tube in enumerate(puzzle.data):
        tube_graphic = TubeGraphic(
            tube=tube,
            tube_x=tube_x,
            tube_y=tube_y,
            tube_graphic_width=TUBE_GRAPHIC_WIDTH,
            tube_graphic_height=TUBE_GRAPHIC_HEIGHT,
            tube_border_width=TUBE_BORDER_WIDTH,
            visual_indicator_offset=TUBE_VISUAL_INDICATOR_OFFSET
        )

        # go to next row
        if multiple_rows and tube_idx == tube_row_delimiter:
            tube_x = multiple_row_offset
            tube_y += TUBE_GRAPHIC_HEIGHT + space_between_tubes
        else:
            tube_x += TUBE_GRAPHIC_WIDTH + space_between_tubes
        tube_graphics.append(tube_graphic)
    return tube_graphics


def detect_tube_selection(tube_graphic):
    # check if current graphic is selected. if so, raises it slightly through TubeGraphic.raise_visual_indicator()
    mouse_focused_on_game = pg.mouse.get_focused() != 0
    left_mouse_clicked = pg.mouse.get_pressed()[0]
    mouse_tube_collision = tube_graphic.tube_graphic.collidepoint(pg.mouse.get_pos())
    tube_empty = tube_graphic.tube.is_empty()

    if mouse_focused_on_game and left_mouse_clicked and mouse_tube_collision and not tube_empty:
        tube_graphic.raise_visual_indicator()


def detect_tube_target_and_deselection(target_tube_graphic: TubeGraphic, selected_tube_graphic: TubeGraphic):
    # liquid cannot be transferred from a tube to itself
    # instead, treat this as deselecting the tube
    if target_tube_graphic.is_selected:  # easier than checking if tube_graphic == selected_tube
        target_tube_graphic.lower_visual_indicator()
        return

    # detect if user is clicking on tube
    mouse_focused_on_game = pg.mouse.get_focused() != 0
    left_mouse_clicked = pg.mouse.get_pressed()[0]
    mouse_tube_collision = target_tube_graphic.tube_graphic.collidepoint(pg.mouse.get_pos())

    if mouse_focused_on_game and left_mouse_clicked and mouse_tube_collision:
        # transfer the liquid if possible
        if selected_tube_graphic.tube.can_move_liquid_into(target_tube_graphic.tube):
            selected_tube_graphic.tube.move_liquid(target_tube_graphic.tube)
            selected_tube_graphic.lower_visual_indicator()
            # post event to redraw the tube colors as the content of the tube has changed
            pg.event.post(pg.event.Event(UPDATE_TUBE_EVENT))


def detect_interactions(tube_graphics: List[TubeGraphic]):
    any_tube_selected = any(tg.is_selected for tg in tube_graphics)
    if any_tube_selected:
        selected_tube_graphic = [tg for tg in tube_graphics if tg.is_selected][0]

    for tube_graphic in tube_graphics:
        # only one tube can be selected at a time
        # if a tube is already selected, watch for another tube selection as the target tube to transfer liquids
        if any_tube_selected:
            # noinspection PyUnboundLocalVariable
            detect_tube_target_and_deselection(tube_graphic, selected_tube_graphic)
        else:
            detect_tube_selection(tube_graphic)


def draw_tube_colors(window, tube_graphic):
    for color_idx, color_rect in enumerate(tube_graphic.color_graphics):
        # draw the color inside the tube's borders
        drawing_last_color = color_idx == len(tube_graphic.tube.data) - 1

        # draw the section of liquid
        corresponding_color = tube_graphic.tube.data[color_idx]
        color = COLORS[corresponding_color]
        if drawing_last_color:
            pg.draw.rect(window, color, color_rect,
                         border_bottom_left_radius=TUBE_BORDER_RADIUS,
                         border_bottom_right_radius=TUBE_BORDER_RADIUS)
        else:
            pg.draw.rect(window, color, color_rect)


def draw_tubes(window, tube_graphics: List[TubeGraphic]):
    for tube_graphic in tube_graphics:
        # draw the tube outline
        pg.draw.rect(window, COLORS["BLACK"], tube_graphic.tube_graphic, width=TUBE_BORDER_WIDTH,
                     border_bottom_left_radius=TUBE_BORDER_RADIUS, border_bottom_right_radius=TUBE_BORDER_RADIUS)

        # hide the top border of the tube, so it appears open
        pg.draw.rect(window, BACKGROUND_COLOR, tube_graphic.tube_graphic_top_cover)

        # draw the colors inside the tube
        draw_tube_colors(window, tube_graphic)


def draw_move_text(window, move_count: int):
    font = pg.font.SysFont('helvetica', 25)
    draw_text = font.render("Move Count: " + str(move_count), True, COLORS["BLACK"])
    padding = 20
    window.blit(draw_text, (padding, HEIGHT - padding - draw_text.get_height()))


def draw_window(window, tube_graphics: List[TubeGraphic], move_count: int):
    # set background color
    window.fill(BACKGROUND_COLOR)

    draw_move_text(window, move_count)
    draw_tubes(window, tube_graphics)


# occurs outside main draw_window game loop
def draw_text_center_screen(window, text: str, font: str = 'comicsans', font_size: int = 100):
    font = pg.font.SysFont(font, font_size)
    draw_text = font.render(text, True, COLORS["WHITE"])
    window.blit(draw_text, ((WIDTH - draw_text.get_width()) // 2, (HEIGHT - draw_text.get_height()) // 2))
    pg.display.update()
