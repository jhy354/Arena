from os import walk

import pygame

from engine.settings import *


class Debug:

    def __init__(self, debug_mode=False):
        self.debug_mode = debug_mode

    def __lshift__(self, other):
        if self.debug_mode:
            print(other, end="")

        return self

    def div(self):
        if self.debug_mode:
            print("-" * 30)


class Timer:

    def __init__(self, duration, func=None):
        self.duration = duration
        self.func = func
        self.start_time = 0
        self.active = False

    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = 0

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.duration and self.active:
            self.deactivate()
            # if self.func is not None:
            if self.func:
                self.func()


def import_folder(path, size=(0, 0)):
    """
    将目录中所有图片文件导入为 surface 对象
    在需要使用目录中所有图片时使用
    保留 alpha通道
    """
    surface_list = []

    for folder_name, sub_folder, img_files in walk(path):
        for image in img_files:
            full_path = path + "/" + image
            Debug(DEBUG_MODE) << full_path << "\n"

            # convert_alpha() 优化性能 保留 alpha通道
            image_surf = pygame.image.load(full_path).convert_alpha()

            # 重置尺寸
            if size[0] != 0:
                image_surf = pygame.transform.scale(image_surf, size)

            surface_list.append(image_surf)

        Debug(DEBUG_MODE) << "Imported Folder " << path << "\n"
        Debug(DEBUG_MODE).div()

    return surface_list


def custom_load(image_path, size=(0, 0), silent=False):
    """
    带缩放图片大小的导入
    保留 alpha通道
    """
    surf = pygame.image.load(image_path).convert_alpha()

    if size[0] != 0:
        surf = pygame.transform.scale(surf, size)

    if not silent:
        Debug(True) << "Imported " << image_path << "\n"
        Debug(True).div()

    return surf


def render_text(content, font_name, size, color):
    """
    生成文本的 surface 对象
    """
    font = pygame.font.SysFont(font_name, size)
    text = font.render(content, True, color)
    return text
