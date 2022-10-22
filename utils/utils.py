import pygame


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


def render_text(content, font_name, size, color):
    """
    生成文本的 surface 对象
    """
    font = pygame.font.SysFont(font_name, size)
    text = font.render(content, True, color)
    return text

