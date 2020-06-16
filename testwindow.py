import random
import time
import math
from functools import partial

from kivy.config import Config
from kivy.config import ConfigParser
Config.set('widgets', 'scroll_timeout', '10')
Config.write()
Config.set('widgets', 'scroll_distance', '400')
Config.write()
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.scrollview import ScrollView
from kivy.uix.settings import Settings
from kivy.uix.settings import SettingsWithSidebar
from kivy.uix.image import Image
from kivy.uix.progressbar import ProgressBar
from kivy.graphics import *
from kivy.uix.modalview import ModalView
from kivy.uix.checkbox import CheckBox
from kivy.properties import StringProperty


class LoginScreen(GridLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.btn = Button(
            text='booty',
            disabled=True,
            background_disabled_normal='materialimg/popup.jpg'
        )

        self.add_widget(self.btn)


class MyApp(App):
    def __init(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)

    def build(self):
        return LoginScreen()


if __name__ == '__main__':

    MyApp().run()