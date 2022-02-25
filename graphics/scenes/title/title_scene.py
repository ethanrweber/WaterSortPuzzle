import pygame

from graphics.scenes.puzzle import puzzle_scene
from graphics.scenes.scene import SceneBase
from puzzles import puzzles


class TitleScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Move to the next scene when the user pressed Enter
                self.SwitchToScene(puzzle_scene.PuzzleScene(puzzles.puzzle_100))

    def Update(self):
        pass

    def Render(self, screen, events):
        # For the sake of brevity, the title scene is a blank red screen
        screen.fill((255, 0, 0))
