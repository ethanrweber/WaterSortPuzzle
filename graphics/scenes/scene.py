# Centralized Scene Logic
# used from https://nerdparadise.com/programming/pygame/part7
# The first half is just boiler-plate stuff...

import pygame
import logging

from constants import WIDTH, HEIGHT, FPS, DEBUG_LOGGING
import graphics.scenes.title.title_scene as title_scene


class SceneBase:
    def __init__(self):
        self.next = self

    def ProcessInput(self, events, pressed_keys):
        print("uh-oh, you didn't override this in the child class")

    def Update(self):
        print("uh-oh, you didn't override this in the child class")

    def Render(self, screen, events):
        """
        events *really* shouldn't be used in the Render function,
        but it's necessary for pygame_widgets to work as it handles everything at once
        :param screen:
        :param events:
        :return:
        """

        print("uh-oh, you didn't override this in the child class")

    def ClearWidgets(self):
        print("uh-oh, you didn't override this in the child class")

    def SwitchToScene(self, next_scene):
        self.ClearWidgets()
        self.next = next_scene

    def Terminate(self):
        logging.info("Terminate Scene (end game)")
        self.SwitchToScene(None)


def run_game(width, height, fps, starting_scene):
    logging.info("run game")
    pygame.init()
    pygame.font.init()
    logging.debug(f"instantiate game window: {width}x{height}")
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    active_scene = starting_scene

    logging.info("begin main game loop")
    while active_scene is not None:
        active_scene_class_name = active_scene.__class__.__name__
        logging.info("tick scene: " + active_scene_class_name)

        pressed_keys = pygame.key.get_pressed()

        # Event filtering
        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            if event.type == pygame.QUIT:
                quit_attempt = True
            elif event.type == pygame.KEYDOWN:
                alt_pressed = pressed_keys[pygame.K_LALT] or \
                              pressed_keys[pygame.K_RALT]
                if event.key == pygame.K_ESCAPE:
                    quit_attempt = True
                elif event.key == pygame.K_F4 and alt_pressed:
                    quit_attempt = True

            if quit_attempt:
                logging.info("attempting to quit game")
                active_scene.Terminate()
            else:
                filtered_events.append(event)

        logging.info(active_scene_class_name + ": ProcessInput()")
        active_scene.ProcessInput(filtered_events, pressed_keys)

        logging.info(active_scene_class_name + ": Update()")
        active_scene.Update()

        logging.info(active_scene_class_name + ": Render()")
        active_scene.Render(screen, filtered_events)

        active_scene = active_scene.next

        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    # instantiate logger
    logging_level = logging.DEBUG if DEBUG_LOGGING else logging.WARNING
    logging.basicConfig(filename="water_sort_puzzle.log", level=logging_level)
    logging.info("Run game")
    # gameplay
    run_game(WIDTH, HEIGHT, FPS, title_scene.TitleScene())
    logging.info("End game")
