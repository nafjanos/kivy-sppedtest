import speedtest
import threading

from kivy.config import Config
Config.set('graphics', 'resizable', False)
# Set the icon file path
icon_path = 'icon.png'

# Set the icon in the Config
Config.set('kivy', 'window_icon', icon_path)

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.button import Button



class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MyBoxLayout, self).__init__(**kwargs)

        self.img = AsyncImage(source='bg.png', size_hint=(0, 0), pos_hint= {'center_x': 0.5})
        self.add_widget(self.img)
        self.img.on_load = self.loaded
        #self.img.allow_stretch: True
        #self.img.keep_ratio: True

        self.button = Button(size_hint=(.5, .5), pos_hint= {'center_x': 0.5})
        self.add_widget(self.button)
        self.button.border = [0,0,0,0]
        self.button.background_normal = 'go-up.png'
        self.button.background_down = 'go-down.png'
        self.button.background_disabled_normal = 'loading.png'
        self.button.on_press = self.go_test
        
    def loaded(self):
        self.button.disabled = False

    def go_test(self):
        self.button.size_hint = (.1, .1)
        self.button.background_normal = 'go-up.png'
        self.button.background_down = 'go-down.png'
        self.img.size_hint = (.7, .8)
        self.img.source = 'loading.gif'
        x = threading.Thread(target=self.speed_test)
        x.start()


    def speed_test(self):
        self.button.disabled = True
        test = speedtest.Speedtest(secure=True)
        test.download()
        test.upload()
        result = test.results.share()
        self.img.source = result
        


class BoxLayoutApp(App):
    title = "Kivy Speedtest"
    def build(self):
        Window.clearcolor = (20/255,21/255,36/255)
        Window.size=(1000, 700)
        box_layout = MyBoxLayout(orientation='vertical', size_hint=(1, 1))
        
        return box_layout

if __name__ == '__main__':
    BoxLayoutApp().run()