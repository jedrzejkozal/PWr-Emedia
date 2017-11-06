from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import matplotlib.pyplot as plt
import numpy as np

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

    def display_samples_fft(self, samples, sample_rate,num_channels):
        #time vector
        n = len(samples)
        k = np.arange(n)
        T = float(n) / sample_rate
        freq = k/T
        freq = freq[range(n/2)]

        fig, ax = plt.subplots(num_channels, 1)

        for i in range(0,num_channels):
            plt.figure(1)
            #calculate fft and normalize results
            y = np.fft.fft(samples[:,1])/n
            y = y[range(n/2)]
            ax[i].plot(freq,abs(y))
            ax[i].set_title('Channel {} FFT'.format(i+1))
            ax[i].set_xlabel('Freq (Hz)')
        plt.show();


    def load(self, path, filename):
        h = HeaderBuilderWAV()
        h.readHeader(os.path.join(path, filename[0]))
        self.text_input.text = str(h.header)
        sample_rate = h.header.get_property("SampleRate")
        num_channels = h.header.get_property("NumChannels")

        # display first 1000 samples
        self.display_samples_fft(h.data[0:1000],sample_rate,num_channels);

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
