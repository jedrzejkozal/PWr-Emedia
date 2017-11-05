from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from HeaderBuilderWAV import *

import os


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class ErrorDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class Root(FloatLayout):
    loadfile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def __init__(self):
        super(self.__class__, self).__init__()
        self.isLoaded = False

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        h = HeaderBuilderWAV()
        h.readHeader(os.path.join(path, filename[0]))
        self.text_input.text = str(h.header)
        self.dismiss_popup()
        self.isLoaded = True

    def cos(self):
        self.dismiss_popup()

    def fourier_transform(self):
        if not self.isLoaded:
            content = ErrorDialog(load=self.cos, cancel=self.dismiss_popup)
            self._popup = Popup(title="File not Loaded!", content=content,
                                size_hint=(0.9, 0.9))
            self._popup.open()

        else:
            print 'fourier'


class Wavreader(App):
    pass


Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('ErrorDialog', cls=ErrorDialog)


if __name__ == '__main__':
    Wavreader().run()
