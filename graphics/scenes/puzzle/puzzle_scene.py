import pygame as pg
import pygame.display
import pygame_widgets
import logging

from pygame_widgets import WidgetHandler
from pygame_widgets.button import Button

from constants import UPDATE_TUBE_EVENT, HINT_BUTTON_EVENT, WIDTH, HEIGHT, DEBUG_LOGGING
from data.graph import Graph
from graphics.scenes.puzzle.puzzle_renderer import create_tube_graphics, detect_interactions, draw_window, draw_text_center_screen
from graphics.scenes.scene import SceneBase
from data.node import Node
from graphics.scenes.title import title_scene

class_name = "PuzzleScene"

class PuzzleScene(SceneBase):
    def __init__(self, game_puzzle: Node):
        SceneBase.__init__(self)

        logging.info(class_name + ' init with puzzle:')
        logging.debug(game_puzzle)

        # pygame setup
        pg.display.set_caption("Water Sorting Puzzle - " + str(game_puzzle.num_id))

        # Scene content
        logging.info('create tube graphics')
        self.puzzle = game_puzzle
        self.tube_graphics = create_tube_graphics(game_puzzle)

        # default initializations
        self.move_counter = 0

        # auto solver stuff
        self.puzzle_solved = False
        self.puzzle_failed = False
        self.hint_button_pressed = False
        self.puzzle_solver_attempted = False
        self.solved_node_move_index = 0
        self.solved_node = None

        # widgets
        self.hint_button = None

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                logging.debug("MOUSEBUTTONDOWN detected")
                detect_interactions(self.tube_graphics)

            # this event is fired when liquid is transferred from one tube to another
            if event.type == UPDATE_TUBE_EVENT:
                logging.debug("UPDATE_TUBE_EVENT detected")
                self.move_counter += 1

            if event.type == HINT_BUTTON_EVENT:
                logging.debug("HINT_BUTTON_EVENT detected")
                self.hint_button_pressed = True

    def Update(self):
        self.puzzle_solved = self.puzzle.is_solved()
        logging.info(class_name + ": is puzzle solved?: " + str(self.puzzle_solved))

        # if the hint button has been pressed and the puzzle has been created but not yet solved, solve it
        if self.hint_button_pressed and not self.puzzle_solver_attempted:
            logging.info("attempting to solve puzzle...")
            self.puzzle_solver_attempted = True
            result, final_node = Graph.solve(self.puzzle)
            if result:
                logging.info("solved puzzle")
                self.solved_node = final_node
            else:
                logging.info("failed to solve puzzle")
                self.puzzle_failed = True

        # if the puzzle has been solved (through the hint button), display each move for 1.5s
        if self.hint_button_pressed and \
                self.solved_node is not None and \
                self.solved_node_move_index < len(self.solved_node.move_list):

            logging.info("solved puzzle: making move")

            i, j = self.solved_node.move_list[self.solved_node_move_index]
            logging.debug(f"Move {self.solved_node_move_index} of {len(self.solved_node.move_list)}: "
                          f"Transfer liquid from {i} to {j}")
            self.tube_graphics[i].tube.move_liquid(self.tube_graphics[j].tube)

            # update move counter on screen and iterate to the next step to solve
            self.move_counter += 1
            self.solved_node_move_index += 1

            # reset hint button so it can be pressed again
            self.hint_button_pressed = False

    def Render(self, screen, events):
        # DON'T USE EVENTS HERE except for pygame_widgets

        # initialize solve button widget
        if self.hint_button is None:
            logging.info("instantiate solve_button")
            self.hint_button = Button(
                screen, (WIDTH * 9 // 10), (HEIGHT * 9 // 10), (WIDTH * 1 // 15), (HEIGHT * 1 // 15),
                text="Hint", fontSize=30, onClick=lambda: pg.event.post(pg.event.Event(HINT_BUTTON_EVENT))
            )
            logging.debug(self.hint_button)

        logging.info("draw_window")
        draw_window(screen, self.tube_graphics, self.move_counter)

        if self.puzzle_solved:
            logging.info("puzzle_solved - win! draw win text on screen and Terminate()")
            draw_text_center_screen(screen, 'YOU WON!')
            pg.time.delay(5000)
            self.SwitchToScene(title_scene.TitleScene())

        if self.puzzle_failed:
            logging.info("puzzle_failed - lose :( draw lose text on screen and Terminate()")
            draw_text_center_screen(screen, 'Puzzle failed, restart!')
            pg.time.delay(5000)
            self.SwitchToScene(title_scene.TitleScene())

        # events shouldn't be handled here but this is necessary:
        # if pygame_widgets.update is called in the Update method, the button will be drawn behind the screen
        pygame_widgets.update(events)

        pygame.display.update()

    def ClearWidgets(self):
        logging.info(f"{class_name}: Clear Widgets")
        widgets = WidgetHandler.getWidgets()
        widgets.remove(self.hint_button)
