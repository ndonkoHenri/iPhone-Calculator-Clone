from kivymd.app import MDApp
from kivy.uix.textinput import TextInput
from kivymd.uix.button import MDIconButton
from kivymd.uix.screen import MDScreen
from kivy.utils import get_color_from_hex
import os
import platform
import re

# This is needed for supporting Windows 10 with OpenGL < v2.0
if platform.system() == "Windows":
    os.environ["KIVY_GL_BACKEND"] = "angle_sdl2"


# todo: look for fonts and icons for the buttons

class iCalculator(MDApp):  # NOQA: N801
    def __init__(self, **kwargs):
        super(iCalculator, self).__init__(**kwargs)
        # a title for the window. Only on PC's
        self.title = "iCalculator"

        self.theme_cls.theme_style = "Dark"


class HomeScreen(MDScreen):
    pass


class FloatInput(TextInput):
    """
    A class for the input receiver....(The calculation field)
    """
    result = 0
    pat = re.compile('[^0-9]')
    all_arithmetic_operators = ['+', '-', '*', '/']

    def insert_text(self, substring, from_undo=False):
        """
        Overrides the original function. It filters the characters sent into the calculation Field,
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
        """
        The add_to_input function is called when a button is pressed.
        It performs some validation checks on the text of the pressed button and that in the validation field.

        Args:
            instance: the instance of the pressed button to this function(it contains everything about that button)
        """
        btn_val_str = instance.value_str  # the value(string value) of the pressed button
        if not self.length_checker():

            if (self.text == '0') or \
                    (self.text.upper() == "ERROR") or \
                    (self._eval_text == str(self.result) and (btn_val_str not in self.all_arithmetic_operators)):
                # if the text in the calculation field is '0' or 'ERROR', then remove it and start from fresh
                self.text = ''
                self._eval_text = ""

            if btn_val_str == '=':
                # if the pressed button is the 'equal' button, then we evaluate
                self.evaluate()
                return  # we stop and don't go any further

            if self.check_last_operator():
                # if the last element of self._eval_text is an arithmetic operator (check function for details)
                if btn_val_str in self.all_arithmetic_operators:
                    # if the last element is an operator and the currently passed element is also an operator
                    self._eval_text = self._eval_text.replace(self._eval_text[-1], btn_val_str)
                else:
                    # if the last element is an operator but the currently passed element is NOT an operator
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
        The evaluate function is called when the user presses the equal button.
        It evaluates the expression in self._eval_text and puts it in self.text,
        and then resets _eval_text to an empty string.
        """

        # The try-except here plays an important role in error handling.
        # It helps the app not die because of some calculation errors!
        try:
            self.result = eval(self._eval_text.lstrip('0'))
            print(self._eval_text.lstrip('0'), self.result)
            self.text, self._eval_text = str(self.result), str(self.result)
        except:
            # if an error occurs, we let the user know about it
            self.text, self._eval_text = "ERROR", ""

    def check_last_operator(self):
        """
        The check_last_operator function checks if the last button pressed is an arithmetic operator.
        If it is, then it returns True. If not, then it returns False.

        Returns:
            True if the last button pressed is that of an arithmetic operator
        """

        if self._eval_text and self._eval_text[-1] in self.all_arithmetic_operators:
            return True
        else:
            return False

    def clear(self):
        """
        The clear function clears the values in the calculation field.
        """

        self.text = "0"
        self._eval_text = ''

    def length_checker(self):
        """
        The length_checker function checks the length of the text in the calculation field.
        If it is >=9, then it returns True. If not, then False.
        This prevents the values crossing the field or be unseen by the user.

        Returns:
            True if the length of the text in the calculation field is >= 9
        """
        if len(self.text) >= 9:
            return True
        else:
            return False


class OrangeButton(MDIconButton):
    # colors shown initially
    initial_colors = {"md_bg_color": get_color_from_hex("#FF9500"), "icon_color": get_color_from_hex("#FFFFFF")}
    # colors to use when the button is pressed
    on_press_colors = {"md_bg_color": get_color_from_hex("#FFFFFF"), "icon_color": get_color_from_hex("#FF9500")}

    def change_colors(self, *args):
        """
        The change_colors function is used to change the colors of the buttons when they are pressed.
        The function takes in a list of arguments(all orangeButtons except the pressed one)
        and tries to imitate the toggle button functionality. When one is on/pressed, the others are unpressed or off.

        Args:
            *args: all the OrangeButtons except the one pressed
        """

        for x in args:
            # some parameters are changed to obtain the desired effect
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
