from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from data_model import conf

Builder.load_string(
"""

<MainScreen>:
    recycle_view: recycle_view
    items_box: items_box
    BoxLayout:
        orientation: 'vertical'
        background_normal: ''
        canvas.before:
            Color:
                rgba: [1,1,1,1]
            Rectangle:
                size: self.size
                pos: self.pos

        Label:
            text_size: self.size
            valign: 'middle'
            text: "Транспортные средства"
            bold: True
            font_name: "Candara"
            padding_x: '16sp'
            font_size: '24sp'
            color: [0,0,0,1]
            size_hint: 1, 0.08
            background_color: (126/255, 188/255, 137/255, 1)
			canvas.before:
				Color:
					rgba: self.background_color
				Rectangle:
					size: self.size
					pos: self.pos
    
        RecycleView:
            id: recycle_view
            size_hint: 1, 0.84
            viewclass: "ListItem"

            RecycleBoxLayout:
                id: items_box
                orientation: "vertical"
                default_size_hint: 1, None
                size_hint: 1, None
                height: self.minimum_height

        BoxLayout:
            orientation: 'vertical'
            size_hint: 1, 0.1

            Widget:
                size_hint: 1, 0.1
                background_normal: ''

            Button:
                text: 'ЗАПРОСИТЬ ПРОВЕРКУ'
                size_hint: 0.9, 0.85
                pos_hint: {"x":.05, "y":.5}
                font_name: "Candara"
                italic: True
                font_size: '18sp'
                color: [0,0,0,1]
                background_normal: ''
                background_color: (126/255, 188/255, 137/255, 1)
                canvas.before:
                    Color:
                        rgba: self.background_color if self.state=='normal' else [193/255, 219/255, 179/255, 1]
                    Rectangle:
                        size: self.size
                        pos: self.pos
            
            Widget:
                size_hint: 1, 0.15
                background_normal: ''

<ListItem@BoxLayout>:
    orientation: "horizontal"
    size_hint: 1, None
    title: ''
    Label:
        background_normal: ''
        font_name: "Arial"
        font_size: '14sp'
        padding_x: '30sp'
        bold: True
        canvas.before:
            Rectangle:
                pos: self.pos
                size: self.size
                source: 'res/shadow.png'
        text: root.title
        color: [0,0,0,1]
        size_hint_x: 0.9
        text_size: self.size
        valign: "middle"

""")


class MainScreen(Screen, RecycleView):
    recycle_view = ObjectProperty(None)
    items_box = ObjectProperty(None)

    def __init__(self, lable_text, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        for i in range(0,len(lable_text)):
            self.recycle_view.data.append({'title': lable_text[i]})

    def on_leave(self):
        self.recycle_view.data = []