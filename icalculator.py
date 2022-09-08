import re

from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.screen import MDScreen
from kivy.utils import get_color_from_hex
import os
import platform

from kivy.core.window import Window
from kivymd.app import MDApp

# This is needed for supporting Windows 10 with OpenGL < v2.0
if platform.system() == "Windows":
    os.environ["KIVY_GL_BACKEND"] = "angle_sdl2"
# todo: solve clear button and big values
# todo: font for the buttons

class iCalculator(MDApp):  # NOQA: N801
    def __init__(self, **kwargs):
        super(iCalculator, self).__init__(**kwargs)
        # a title for the window. Only on PC's
        self.title = "iCalculator"

        self.theme_cls.theme_style = "Dark"

    def build(self):
        # building of the UI
        return Builder.load_file('icalculator.kv')




class HomeScreen(MDScreen):
    def on_size(self, *args):
        print(self.size)


class FloatInput(TextInput):
    result = 0
    pat = re.compile('[^0-9]')
    all_arithmetic_operators = ['+', '-', '*', '/']


    def insert_text(self, substring, from_undo=False):
        """
        Overrides the original function. It filters the characters sent into the Field,
        allowing only Numbers[0-9] and one dot(.)
        This function was copied from the kivy docs.
        """
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
        btn_val_str = instance.value_str  # the value(a string) of the pressed button
        if not self.length_checker():
            if self.text == '0':
                # if the text in the field is '0', then remove it and start from fresh
                self.text = ''
                self._eval_text = ""

            if btn_val_str == '=':
                # if the pressed button is the 'equal' button, then we evaluate
                self.evaluate()
                return      # we stop and don't go any further

            if self.check_last_operator():
                # if the last element of self._eval_text is an arithmetic operator (check function for details)
                if btn_val_str in self.all_arithmetic_operators:
                    # if the last element is an operator and the currentlu passed element is also an operator
                    self._eval_text = self._eval_text.replace(self._eval_text[-1], btn_val_str)
                else:
                    # if the last element is an operator but the currentlu passed element is NOT an operator
                    self.text = ""
                    self.insert_text(btn_val_str)
                    self._eval_text += btn_val_str

            else:
                # if the last element is NOT an operator
                self.insert_text(btn_val_str)
                self._eval_text += btn_val_str
        else:
            if btn_val_str in self.all_arithmetic_operators:
                if not self.check_last_operator():
                    self._eval_text += btn_val_str
                else:
                    self._eval_text = self._eval_text.replace(self._eval_text[-1], btn_val_str)

    def evaluate(self):

        """
        evaluates what is present in the _eval_text and gives us the result
        """
        self.result = eval(self._eval_text)
        self.text = ''
        self.text = str(self.result)
        # todo: did the below code work
        self._eval_text = self.result

    def check_last_operator(self):
        """
        Check if the value of the last button pressed is that of an arithmetic operator
        """
        if self._eval_text and self._eval_text[-1] in self.all_arithmetic_operators:
            return True
        else:
            return False

    def clear(self):
        self.text = "0"
        self._eval_text = ''

    def length_checker(self):
        """
        The field must have a max value so that the values do not cross the field or be unseen by the user.
        10 in this case.
        """
        if len(self.text) == 9:
            return True
        else:
            return False


class OrangeButton(MDIconButton):
    initial_colors = {"md_bg_color": get_color_from_hex("#FF9500"), "icon_color": get_color_from_hex("#FFFFFF")}
    on_press_colors = {"md_bg_color": get_color_from_hex("#FFFFFF"), "icon_color": get_color_from_hex("#FF9500")}

    def change_colors(self, *args):
        """
        Tries to imitate the toggle buttons functionality. When one is on/pressed, the others become unpressed or off.

        :params args: all the OrangeButtons except the one pressed
        """
        for x in args:
            x.ripple_color = 1, 1, 1, 1
            x.icon_color = self.initial_colors["icon_color"]
            x.md_bg_color = self.initial_colors["md_bg_color"]

        # We make an exception for the equal button since it doesn't have a toggle behaviour.
        # Check an iphone to see this better.
        if self.value_str != "=":

            self.ripple_color = [1.0, 0.5843137254901961, 0.0, 0.5]
            self.md_bg_color = self.on_press_colors["md_bg_color"]
            self.icon_color = self.on_press_colors["icon_color"]



if __name__ == "__main__":
    from kivy import Config
    # we disable a debug mode functionality( comment the line below and do a right-click in window to see more clearly)
    Config.set("input", "mouse", "mouse,disable_multitouch")
    from kivy.core.window import Window
    Window.size = 320, 571
    Window.minimum_height = 465
    Window.minimum_width = 320

    iCalculator().run()