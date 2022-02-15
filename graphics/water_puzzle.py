from typing import List

import pygame as pg

from constants import FPS, COLORS, EMPTY_SYMBOL
from data.node import Node
from data.tube import Tube
from graphics.tube_graphic import TubeGraphic

pg.font.init()

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

# custom events:
UPDATE_TUBE_EVENT = pg.USEREVENT + 1


def create_tube_graphics(puzzle: Node):
    # draw the tubes in start node
    tube_graphics = []

    tube_x = space_between_tubes
    tube_y = HEIGHT // 4
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
            detect_tube_target_and_deselection(tube_graphic, selected_tube_graphic)
        else:
            detect_tube_selection(tube_graphic)


def draw_tube_colors(tube_graphic):
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


def draw_tubes(tube_graphics: List[TubeGraphic]):
    for tube_graphic in tube_graphics:
        # draw the tube outline
        pg.draw.rect(window, COLORS["BLACK"], tube_graphic.tube_graphic, width=TUBE_BORDER_WIDTH,
                     border_bottom_left_radius=TUBE_BORDER_RADIUS, border_bottom_right_radius=TUBE_BORDER_RADIUS)

        # hide the top border of the tube, so it appears open
        pg.draw.rect(window, BACKGROUND_COLOR, tube_graphic.tube_graphic_top_cover)

        # draw the colors inside the tube
        draw_tube_colors(tube_graphic)


def draw_move_text(move_count: int):
    font = pg.font.SysFont('helvetica', 25)
    draw_text = font.render("Move Count: " + str(move_count), True, COLORS["BLACK"])
    padding = 20
    window.blit(draw_text, (padding, HEIGHT - padding - draw_text.get_height()))


def draw_window(tube_graphics: List[TubeGraphic], move_count: int):
    # set background color
    window.fill(BACKGROUND_COLOR)

    draw_move_text(move_count)
    draw_tubes(tube_graphics)

    pg.display.update()


# occurs outside main draw_window game loop
def draw_win_text():
    font = pg.font.SysFont('comicsans', 100)
    draw_text = font.render('YOU WON!', True, COLORS["WHITE"])
    window.blit(draw_text, ((WIDTH - draw_text.get_width()) // 2, (HEIGHT - draw_text.get_height()) // 2))
    pg.display.update()


def main():
    tube_graphics = create_tube_graphics(GAME_PUZZLE)
    move_counter = 0

    # game setup
    clock = pg.time.Clock()
    run = True
    while run:
        clock.tick(FPS)

        game_solved = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                detect_interactions(tube_graphics)
            # this event is fired when liquid is transferred from one tube to another
            if event.type == UPDATE_TUBE_EVENT:
                move_counter += 1
                for tg in tube_graphics:
                    tg.recreate_color_graphics()
                all_solved = all(tg.tube.is_solved() for tg in tube_graphics)
                if all_solved:
                    game_solved = True

        draw_window(tube_graphics, move_counter)

        if game_solved:
            draw_win_text()
            pg.time.delay(5000)
            run = False


if __name__ == '__main__':
    main()
    pg.quit()
