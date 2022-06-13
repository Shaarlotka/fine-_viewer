from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.clock import Clock

from time import time

Builder.load_string('''
<ListScreen>:
    recycle_view: recycle_view
    items_box: items_box
    BoxLayout:
        orientation: "vertical"
        AnchorLayout:
            size_hint_y: 0.1
            padding: self.width*0.1, self.height*0.05
            Label:
                font_size: root.height*0.05
                text: "Some list"
        RecycleView:
            id: recycle_view
            size_hint: 1, 0.9
            viewclass: "ListItem"
            RecycleBoxLayout:
                id: items_box
                orientation: "vertical"
                padding: self.width*0.1, 0
                default_size_hint: 1, None
                size_hint: 1, None
                height: self.minimum_height

<ListItem@BoxLayout>:
    orientation: "horizontal"
    size_hint: 1, None
    height: app.sm.height*0.1
    title: ''
    Label:
        font_size: app.sm.height*0.025
        text: root.title
        size_hint_x: 0.9
        text_size: self.size
        valign: "middle"
    CheckBox:
        size_hint_x: 0.1                   
                    ''')


class ListScreen(Screen):

    recycle_view = ObjectProperty(None)
    items_box = ObjectProperty(None)

    def on_enter(self):
        start = time()
        for i in range(0,50):
            self.recycle_view.data.append({'title': 'item'+str(i)})
        print (time()-start)

    def on_leave(self):
        self.recycle_view.data = []

class ListApp(App):

    sm = ScreenManager()
    screens = {}

    def build(self):
        self.__create_screens()
        ListApp.sm.add_widget(ListApp.screens['list1'])
        #Clock.schedule_interval(self._switch, 1)
        return ListApp.sm

    def _switch(self, *args):
        ListApp.sm.switch_to(ListApp.screens['list1' if ListApp.sm.current != 'list1' else 'list2'])

    def __create_screens(self):
        ListApp.screens['list1'] = ListScreen(name='list1')
        ListApp.screens['list2'] = ListScreen(name='list2')

if __name__ == '__main__':
    ListApp().run()