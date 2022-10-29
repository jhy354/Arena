from os import walk

import pygame

from settings import *
from utils import Debug


def import_folder(path, size=(0, 0)):
    """
    将目录中所有图片文件导入为 surface 对象
    在需要使用目录中所有图片时使用
    """
    surface_list = []

    for folder_name, sub_folder, img_files in walk(path):
        for image in img_files:
            full_path = path + "/" + image
            Debug(DEBUG_MODE) << full_path << "\n"

            # convert_alpha() 优化性能, 但相对于 convert() 保留了透明效果
            image_surf = pygame.image.load(full_path).convert_alpha()

            # 重置尺寸
            if size[0] != 0:
                image_surf = pygame.transform.scale(image_surf, size)

            surface_list.append(image_surf)

        Debug(DEBUG_MODE) << "Imported Folder " << path << "\n"
        Debug(DEBUG_MODE).div()

    return surface_list


def custom_load(image_path, size=(0, 0)):
    surf = pygame.image.load(image_path)
    if size[0] != 0:
        surf = pygame.transform.scale(surf, size)

    return surf
