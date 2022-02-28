import pygame
import pygame_widgets
import logging

from constants import *
from graphics.graphics_objects.puzzle_selection_graphic import PuzzleSelectionGraphic
from graphics.scenes.puzzle import puzzle_scene
from graphics.scenes.scene import SceneBase
from puzzles import puzzles

class_name = "TitleScene"

class TitleScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        logging.info("Setup " + class_name)

        # default variables
        self.puzzle_selection_graphic = None

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == PUZZLE_SELECTION_EVENT:
                logging.info(f"{class_name}: PUZZLE_SELECTION_EVENT detected")

                # puzzle_id is posted as part of the event's data
                puzzle_id = event.__dict__["puzzle_id"]
                logging.info(f"{class_name}: switch to puzzle {puzzle_id}")

                # get puzzle by id and switch to the puzzle scene
                next_puzzle = puzzles.get_puzzle(puzzle_id)
                self.SwitchToScene(puzzle_scene.PuzzleScene(next_puzzle))

    def Update(self):
        pass

    def Render(self, screen, events):
        # background
        screen.fill(BACKGROUND_COLOR)

        # puzzle selection buttons are instantiated here
        if self.puzzle_selection_graphic is None:
            logging.info(f"{class_name}: Setup PuzzleSelectionGraphic")
            self.puzzle_selection_graphic = PuzzleSelectionGraphic(screen)

        # draw puzzle selection background
        pygame.draw.rect(screen, self.puzzle_selection_graphic.mid_background_color,
                         self.puzzle_selection_graphic.mid_background_rect)

        # draw puzzle selection buttons
        pygame_widgets.update(events)

        # draw the arrow buttons on each corner
        pygame.display.update()

    def ClearWidgets(self):
        logging.info(f"{class_name}: Clear Widgets")
        self.puzzle_selection_graphic.clear_widgets()
