from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

from init_screen import InitScreen
from main_screen import MainScreen
from data_model import Conf

class FineApp(App):
    def __init__(self, **kwargs):
        super(FineApp, self).__init__(**kwargs)
        self.data = Conf()

    def build(self):
        sm = ScreenManager()
        sm.add_widget(InitScreen(name='loading'))
        sm.add_widget(MainScreen(self.data, name='main'))

        return sm


if __name__ == "__main__":
    app = FineApp()
    app.run()