from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.properties import NumericProperty, StringProperty
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
import serial
import threading

# Set the app window size for testing (optional)
Window.size = (350, 600)

KV = '''
ScreenManager:
    HomePage:
    PropertyPage:

<HomePage>:
    name: "home"
    FloatLayout:
        Image:
            source: "wallpaper.jpg"
            allow_stretch: True
            keep_ratio: False
            size: self.size
            pos: self.pos
        MDLabel:
            text: "FlowApp"
            halign: "center"
            font_style: "H4"
            size_hint: 1, None
            height: dp(50)
            pos_hint: {"center_x": 0.5, "top": 1}
            md_bg_color: 0.1, 0.5, 0.8, 1
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            padding_y: dp(10)
        BoxLayout:
            orientation: "vertical"
            spacing: dp(20)
            padding: dp(20)
            size_hint: None, None
            size: dp(300), dp(400)
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            MDRaisedButton:
                text: f"Flow Rate: {root.flow_rate} L/s"
                size_hint: None, None
                size: dp(250), dp(50)
                md_bg_color: 1, 1, 1, 1
                text_color: 0, 0, 0, 1
                on_release: app.open_property_page("Flow Rate", root.flow_rate)
            MDRaisedButton:
                text: f"Temperature: {root.temperature} \u00b0C"
                size_hint: None, None
                size: dp(250), dp(50)
                md_bg_color: 1, 1, 1, 1
                text_color: 0, 0, 0, 1
                on_release: app.open_property_page("Temperature", root.temperature)
            MDRaisedButton:
                text: f"Viscosity: {root.viscosity} mPa.s"
                size_hint: None, None
                size: dp(250), dp(50)
                md_bg_color: 1, 1, 1, 1
                text_color: 0, 0, 0, 1
                on_release: app.open_property_page("Viscosity", root.viscosity)
            MDRaisedButton:
                text: f"RPM: {root.rpm}"
                size_hint: None, None
                size: dp(250), dp(50)
                md_bg_color: 1, 1, 1, 1
                text_color: 0, 0, 0, 1
                on_release: app.open_property_page("RPM", root.rpm)

<PropertyPage>:
    name: "property"
    property_name: ""
    property_value: 0

    FloatLayout:
        Image:
            source: "Wallpaper.jpg"
            allow_stretch: True
            keep_ratio: False
            size: self.size
            pos: self.pos
        BoxLayout:
            orientation: "vertical"
            spacing: dp(20)
            padding: dp(20)
            size_hint: None, None
            size: dp(300), dp(300)
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            MDLabel:
                text: root.property_name
                halign: "center"
                font_style: "H5"
            MDTextField:
                id: property_input
                hint_text: "Enter new value"
                text: str(root.property_value)
                mode: "rectangle"
                line_color_focus: app.theme_cls.colors['Amber']['500']
                line_color: app.theme_cls.colors['Amber']['300']
                hint_text_color: app.theme_cls.colors['Amber']['500']
                text_color: app.theme_cls.colors['Amber']['500']
            MDRaisedButton:
                text: "Save"
                size_hint: None, None
                size: dp(250), dp(50)
                md_bg_color: 1, 1, 1, 1
                text_color: 0, 0, 0, 1
                on_release: app.update_property(root.property_name, property_input.text)
            MDRaisedButton:
                text: "Back"
                size_hint: None, None
                size: dp(250), dp(50)
                md_bg_color: 1, 1, 1, 1
                text_color: 0, 0, 0, 1
                on_release: app.change_screen("home")
'''


class HomePage(Screen):
    flow_rate = NumericProperty(10.0)
    temperature = NumericProperty(25.0)
    viscosity = NumericProperty(1.0)
    rpm = NumericProperty(1200.0)


class PropertyPage(Screen):
    property_name = StringProperty()
    property_value = NumericProperty()


class MyApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_string(KV)

    def open_property_page(self, property_name, property_value):
        property_page = self.root.get_screen("property")
        property_page.property_name = property_name
        property_page.property_value = property_value
        self.change_screen("property")

    def update_property(self, property_name, new_value):
        try:
            new_value = float(new_value)
        except ValueError:
            print("Invalid input")
            return

        home_page = self.root.get_screen("home")
        if property_name == "Flow Rate":
            home_page.flow_rate = new_value
        elif property_name == "Temperature":
            home_page.temperature = new_value
        elif property_name == "Viscosity":
            home_page.viscosity = new_value
        elif property_name == "RPM":
            home_page.rpm = new_value

        self.change_screen("home")

    def change_screen(self, screen_name):
        self.root.current = screen_name


if __name__ == "__main__":
    MyApp().run()
