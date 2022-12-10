from engine.utils import custom_load
from engine.utils import Debug
from engine.core.scene import Scene
from engine.widget.sprite import Generic


class AboutPage(Scene):
    """
    关于页面
    """

    def __init__(self):
        super().__init__()

        self.background = Generic(
            pos=BG_POS,
            surf=custom_load(PATH_UI_BG + "2_bg_night.png", BG_SIZE),
            group=[self.all_sprites],
            z=LAYERS["background"]
        )
