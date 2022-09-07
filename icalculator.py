import re

from kivy.uix.textinput import TextInput
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.screen import MDScreen
from kivy.utils import get_color_from_hex

import os
import platform

from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField

# This is needed for supporting Windows 10 with OpenGL < v2.0
if platform.system() == "Windows":
    os.environ["KIVY_GL_BACKEND"] = "angle_sdl2"


class iCalculator(MDApp):  # NOQA: N801
    def __init__(self, **kwargs):
        super(iCalculator, self).__init__(**kwargs)
        Window.soft_input_mode = "below_target"
        self.title = "iCalculator"

        # self.theme_cls.primary_palette = "Gray"
        # self.theme_cls.primary_hue = "400"
        #
        # self.theme_cls.accent_palette = "Amber"
        # self.theme_cls.accent_hue = "500"

        self.theme_cls.theme_style = "Dark"

    def build(self):
        return HomeScreen()


class HomeScreen(MDScreen):
    pass


class FloatInput(TextInput):
    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join(
                re.sub(pat, '', s)
                for s in substring.split('.', 1)
            )
        return super().insert_text(s, from_undo=from_undo)

    def add_to_input(self, instance):
        print(self.text)
        if not self.length_checker():
            if self.text == '0':
                self.text = ''
            num = instance.value_str
            self.insert_text(num)

        else:
            pass

    def clear(self):
        self.text = "0"

    def length_checker(self):
        if len(self.text)==10:
            return True
        else:
            return False


class OrangeButton(MDIconButton):
    initial_colors = {
        "orange": {"md_bg_color": get_color_from_hex("#f1a43c"), "icon_color": get_color_from_hex("#FFFFFF")},
        "black": {"md_bg_color": get_color_from_hex("#333333"), "icon_color": get_color_from_hex("#FFFFFF")},
        "gray": {"md_bg_color": get_color_from_hex("#a5a5a5"), "icon_color": get_color_from_hex("#FFFFFF")}}

    #
    # on_press_colors = {
    #     "orange": {"md_bg_color": get_color_from_hex("#FF9500"), "icon_color": get_color_from_hex("#FFFFFF")},
    #     "black": {"md_bg_color": get_color_from_hex("#FF9500"), "icon_color": get_color_from_hex("#FFFFFF")},
    #     "gray": {"md_bg_color": get_color_from_hex("#FF9500"), "icon_color": get_color_from_hex("#FFFFFF")}}

    # {"md_bg_color": get_color_from_hex("#FFFFFF"), "icon_color": get_color_from_hex("#FF9500")}

    def disable_others(self, instance):
        pass

#
# class BlackButton(MDIconButton):
#     pass
#
# class ASLabel(AutoScaleLabel):
#     pass
