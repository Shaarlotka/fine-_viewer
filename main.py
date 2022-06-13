from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

from init_screen import InitScreen
from main_screen import MainScreen

class FineApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(InitScreen(name='loading'))
        sm.add_widget(MainScreen(name='main'))

        return sm

if __name__ == "__main__":
    app = FineApp()
    app.run()