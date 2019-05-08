from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle
from kivy.properties import ObjectProperty

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.


Builder.load_string("""
<ButImage@ButtonBehavior+AsyncImage>
<TutImage@ButtonBehavior+AsyncImage>
<MenuScreen>:
GridLayout:
    cols: 4
    row_force_default: True
    col_default_width: 175
    row_default_height: 150
    padding: 15
    spacing: 15
    canvas.before:
        BorderImage:
            # BorderImage behaves like the CSS BorderImage
            border: 10, 10, 10, 10
            source: '/Users/clayhigh/Desktop/kivy/aot.png'
            pos: self.pos
            size: self.size
    Button:
        text: 'Goto settings'
        background_color: 1,0,0,0.5
        on_press: root.manager.current = 'settings'
    ButImage:
        on_press: root.manager.current = 'UBW'
        id: but
        size_hint: .5, .5
        opacity: 1 if self.state == 'normal' else .5
        allow_stretch: True
        keep_ratio: False
        source: 'http://s3.amazonaws.com/rapgenius/1361742626_beautiful-ocean-beautiful-pictures-27115524-1440-900.jpg'
        Label:
            center: but.center
            text: "UBW"
            color: 0.78,0.145,0.016,2
    ButImage:
        id: lh
        size_hint: .5, .5
        opacity: 1 if self.state == 'normal' else .5
        allow_stretch: True
        keep_ratio: False
        source: 'http://s3.amazonaws.com/rapgenius/1361742626_beautiful-ocean-beautiful-pictures-27115524-1440-900.jpg'
        Label:
            center: lh.center
            text: "LH 2"
            color: 0,0,0,1
    ButImage:
        id: ttl
        size_hint: .5, .5
        opacity: 1 if self.state == 'normal' else .5
        allow_stretch: True
        keep_ratio: False
        source: 'http://s3.amazonaws.com/rapgenius/1361742626_beautiful-ocean-beautiful-pictures-27115524-1440-900.jpg'
        Label:
            center: ttl.center
            text: "TwTl"
            color: 0,0,0,1
    ButImage:
        id: gris
        size_hint: .5, .5
        opacity: 1 if self.state == 'normal' else .5
        allow_stretch: True
        keep_ratio: False
        source: 'http://s3.amazonaws.com/rapgenius/1361742626_beautiful-ocean-beautiful-pictures-27115524-1440-900.jpg'
        Label:
            center: gris.center
            text: "Gris"
            color: 0,0,0,1
    ButImage:
        id: shig
        size_hint: .5, .5
        opacity: 1 if self.state == 'normal' else .5
        allow_stretch: True
        keep_ratio: False
        source: 'http://s3.amazonaws.com/rapgenius/1361742626_beautiful-ocean-beautiful-pictures-27115524-1440-900.jpg'
        Label:
            center: shig.center
            text: "Shig"
            color: 0,0,0,1
    Button:
        text: 'Test3'
        background_color: 1,0,0,0.5
    Button:
        text: 'Test4'
        background_color: 1,0,0,0.5
    Button:
        text: 'Quit'
        background_color: 1,0,0,0.5
        on_press: App.on_stop

<SettingsScreen>:
GridLayout:
    row_force_default: True
    row_default_height: 100
    cols: 2
    canvas.before:
        BorderImage:
            # BorderImage behaves like the CSS BorderImage
            border: 10, 10, 10, 10
            source: '/Users/clayhigh/Desktop/kivy/ato.jpeg'
            pos: self.pos
            size: self.size
    Button:
        text: 'Button'
        color: 0,0,.5
        background_color: 1,0,0,1
    Button:
        text: 'Back to menu'
        background_color: 1,0,0,1
        on_press: root.manager.current = 'menu'
<UBW>:
GridLayout:
    row_force_default: True
    row_default_height: 100
    cols: 2
    canvas.before:
        Color:
            rgb: .5, .5, .5
        Rectangle:
            pos: self.pos
            size: self.size
        Color:
            rgb: 1, 1, 1
        BorderImage:
            # BorderImage behaves like the CSS BorderImage
            border: 10, 10, 10, 10
            source: '/Users/clayhigh/Desktop/kivy/fsn.jpg'
            pos: self.pos
            size: self.size
    Button:
        text: 'Back to menu'
        color: 0,0,.5
        on_press: root.manager.current = 'menu'
        background_color: 1,0,0,1
    Label:
        id: AName
        text: "F S/N: UBW"
        font_size: '24sp'
""")

# Declare both screens


class MenuScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass


class UBW(Screen):
    pass

# Create the screen manager
sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(SettingsScreen(name='settings'))
sm.add_widget(UBW(name='UBW'))


class TestApp(App):

    def build(self):
        return sm

    if __name__ == '__main__':
        TestApp().run()