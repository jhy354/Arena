import sys

import pygame

from settings import *
from utils import Debug
from scene import PlayGround
from scene import StartMenu


class Game:

    def __init__(self):
        # * Pygame Init * #
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption(CAPTION)
        self.screen = pygame.display.set_mode(SCR_SIZE)
        self.clock = pygame.time.Clock()
        Debug(DEBUG_MODE).div()

        self.scenes = self.load_scenes()
        self.scenes["start_menu"].activate()

        Debug(True) << "Inited Game" << "\n"
        Debug(True).div()

    @staticmethod
    def load_scenes():
        scenes = {}

        start_menu = StartMenu()
        play_ground = PlayGround()

        scenes["start_menu"] = start_menu
        scenes["play_ground"] = play_ground

        return scenes

    def run(self):
        # * MAIN LOOP * #
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick(FPS) / 1000
            self.check_scenes(dt)
            self.switch_scenes(dt)
            pygame.display.update()

    def check_scenes(self, dt):
        for scene in self.scenes.values():
            if scene.active:
                scene.run(dt)

    def switch_scenes(self, dt):
        """
        场景转换的条件及控制
        """
        if self.scenes["start_menu"].start_button.clicked:
            self.scenes["start_menu"].deactivate()
            self.scenes["play_ground"].activate()
            self.scenes["start_menu"].start_button.clicked = False


if __name__ == "__main__":
    game = Game()
    game.run()
