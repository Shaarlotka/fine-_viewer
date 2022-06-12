from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivy.lang import Builder
from model import conf

Builder.load_string(
"""
<InitScreen>:
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'center'
        canvas:
            Color:
                rgb: [193/255, 219/255, 179/255, 1]
            Rectangle:
                pos: self.pos
                size: self.size
        Image:
            source: 'car-wireless.png'
            size: [200, 200]

""")

class InitScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_state = conf()

    def switchToNextScreen(self):
      self.parent.current = 'LoadingScreen'