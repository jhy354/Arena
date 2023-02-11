from engine.settings import *
from engine.widget.sprite import Generic
from engine.widget.sprite import UIGroup


class DisplayCase(UIGroup):
    """
    展示柜
    循环轮流展示角色皮肤
    """

    def __init__(self, start_pos, surf_list, group, z=LAYERS["ui"]):
        super().__init__(group)
        self.start_pos = start_pos
        self.surf_list = surf_list
        self.sprite = None

        self.play_speed = 0.5
        self.start_speed = 9.5
        self.start_speed_a = -0.1
        self.start_alpha = 50
        self.alpha_speed = 1.1

        self.speed = self.start_speed
        self.speed_a = self.start_speed_a
        self.alpha = self.start_alpha
        self.image_index = 0

        self.z = z
        self.active = False

    def setup(self):
        super().setup()

        self.change_image()

    def change_image(self):

        self.sprite = Generic(
            pos=self.start_pos,
            surf=self.surf_list[self.image_index],
            group=[self.group],
            z=LAYERS["ui"]
        )

        self.image_index += 1
        self.image_index %= len(self.surf_list)

    def update(self):
        if self.active:

            if self.speed_a > 0:  # 加速
                if self.alpha - 1 >= 0:
                    self.alpha -= self.alpha_speed
            else:  # 减速
                if self.alpha + self.alpha_speed <= 255:
                    self.alpha += self.alpha_speed
            if self.speed < 0.2:
                self.alpha = 255
            self.sprite.image.set_alpha(self.alpha)

            self.sprite.rect.y += self.speed * self.play_speed
            if self.speed + self.speed_a < 0:
                self.speed_a = -self.speed_a
                self.speed = 0
            self.speed += self.speed_a * self.play_speed

            if self.sprite.rect.y >= SCR_SIZE[1]:
                self.alpha = self.start_alpha
                self.change_image()
                self.sprite.rect.y = self.start_pos[1]
                self.speed = self.start_speed
                self.speed_a = self.start_speed_a
