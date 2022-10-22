from os import walk

import pygame

from settings import *
from utils import Debug


def import_folder(path) -> list[pygame.surface]:
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
            surface_list.append(image_surf)

        Debug(DEBUG_MODE) << "Imported Folder " << path << "\n"
        Debug(DEBUG_MODE).div()

    return surface_list
