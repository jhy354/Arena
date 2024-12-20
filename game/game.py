import sys
from random import randint

import pygame

from engine.settings import *
from engine.utils import Debug
from engine.utils import custom_load
from game.scenes import StartMenu
from game.scenes import AboutPage
from game.scenes import StartPlayGround
from game.scenes import StartLevel
from game.scenes import StartPractice


class Game:

    def __init__(self, server_ip):
        self.server_ip = server_ip

        # * Pygame Init * #
        pygame.init()
        Debug(True).div()
        pygame.font.init()
        pygame.display.set_caption(CAPTION)
        self.screen = pygame.display.set_mode(SCR_SIZE)
        pygame.display.set_icon(custom_load(r"./logo.ico", (16, 16)))
        self.clock = pygame.time.Clock()

        self.scenes = self.load_scenes()
        self.scenes["start_menu"].activate()

        Debug(True, highlight=True) << "Game Inited"
        Debug(True).div()

    def load_scenes(self):
        scenes = {}

        start_menu = StartMenu()
        about_page = AboutPage()
        play_ground = StartPlayGround(self.server_ip, randint(0, 3), randint(0, 3))
        level = StartLevel(1, 0)
        practice = StartPractice(randint(0, 3), randint(0, 3))

        scenes["start_menu"] = start_menu
        scenes["about_page"] = about_page
        scenes["play_ground"] = play_ground
        scenes["level"] = level
        scenes["practice"] = practice
        Debug(DEBUG_MODE, highlight=True) << f"{len(scenes)} SCENE HAS BEEN INITED"
        Debug(DEBUG_MODE).div()
        # print(scenes)

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
            self.switch_scenes()
            pygame.display.update()

    def check_scenes(self, dt):
        for scene in self.scenes.values():
            if scene.active:
                scene.run(dt)

    def switch_scenes(self):
        """
        场景转换的条件及控制
        """

        if self.scenes["start_menu"].start_button.clicked:
            self.scenes["start_menu"].deactivate()
            self.scenes["level"].activate()
            self.scenes["start_menu"].start_button.clicked = False

        if self.scenes["start_menu"].about_button.clicked:
            self.scenes["start_menu"].deactivate()
            self.scenes["about_page"].activate()
            self.scenes["start_menu"].about_button.clicked = False

        if self.scenes["about_page"].active:
            if self.scenes["about_page"].back_button.clicked:
                self.scenes["about_page"].deactivate()
                self.scenes["start_menu"].activate()
                self.scenes["about_page"].back_button.clicked = False

        if self.scenes["start_menu"].arena_button.clicked:
            self.scenes["start_menu"].deactivate()
            self.scenes["play_ground"].connect_server()
            self.scenes["play_ground"].activate()
            self.scenes["start_menu"].arena_button.clicked = False

        if self.scenes["start_menu"].practice_button.clicked:
            self.scenes["start_menu"].deactivate()
            self.scenes["practice"].activate()
            self.scenes["start_menu"].practice_button.clicked = False

        if self.scenes["start_menu"].quit_button.clicked:
            pygame.quit()
            sys.exit()
