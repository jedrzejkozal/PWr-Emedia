from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from enum import Enum
from RSA import RSA
from kivy.uix.label import Label
from kivy.uix.button import Button
import matplotlib.pyplot as plt
import numpy as np
import struct

from HeaderBuilderWAV import *
from HeaderBuilderBMP import *

import os

class FILETYPE(Enum):
    WAV = 1
    BMP = 2
    UNKNOWN = 3

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class ErrorDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class Root(FloatLayout):
    loadfile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    text_input2 = ObjectProperty(None)
    text_input3 = ObjectProperty(None)
    
    def __init__(self):
        super(self.__class__, self).__init__()
        self.isLoaded = False
        self.loaded_file = FILETYPE.UNKNOWN
        self.h = ''
        self.rsaModule = RSA()

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        if filename[0][-4:] == ".wav":
            self.h = HeaderBuilderWAV()
            self.loaded_file = FILETYPE.WAV
        elif filename[0][-4:] == ".bmp":
            self.h = HeaderBuilderBMP()
            self.loaded_file = FILETYPE.BMP
        else:
            raise ValueError('Not known extension of file')
        self.h.readHeader(os.path.join(path, filename[0]))
        self.text_input.text = str(self.h.header)
        self.dismiss_popup()
        self.isLoaded = True

    def cos(self):
        self.dismiss_popup()

    def display_wav_fft(self, samples, sample_rate,num_channels,fignum):
        #time vector
        n = len(samples)
        k = np.arange(n)
        T = float(n) / sample_rate
        freq = k/T
        freq = freq[range(n/2)]

        fig, ax = plt.subplots(num_channels, 1)


        for i in range(0,num_channels):
            plt.figure(fignum)

            #calculate fft and normalize results
            if num_channels is 1:
                y = np.fft.fft(samples) / n
                y = y[range(n / 2)]
                plt.plot(freq,abs(y))
                plt.title('Channel {} FFT'.format(i+1))
                plt.xlabel('Freq (Hz)')
            else:
                y = np.fft.fft(samples[:,i])/n
                y = y[range(n/2)]
                ax[i].plot(freq,abs(y))
                ax[i].set_title('Channel {} FFT'.format(i+1))
                ax[i].set_xlabel('Freq (Hz)')

    def display_bmp_fft(self, samples):
        plt.figure(1)
        fft = fftpack.fft2(samples)
        plt.imshow(np.abs(np.fft.fftshift(fft)), interpolation='nearest')
        plt.show()

    def fourier_transform(self):
        if not self.isLoaded:

            content = ErrorDialog(load=self.cos, cancel=self.dismiss_popup)
            self._popup = Popup(title="File not Loaded!", content=content,
                                size_hint=(0.9, 0.9))
            self._popup.open()

            #return Button(text='Hello World')
        else:
            if self.loaded_file is FILETYPE.WAV :
                sample_rate = self.h.header.get_property("SampleRate")
                num_channels = self.h.header.get_property("NumChannels")
                self.display_wav_fft(self.h.data[0:1000],sample_rate,num_channels,1);
                plt.show()
            elif self.loaded_file is FILETYPE.BMP:
                self.display_bmp_fft(self.h.data)
                #rsaModule = RSA()
                #enc = rsaModule.encrypt(self.h.data)
                #dec = rsaModule.decrypt(enc)
                #if (self.h.data==dec).all:
                #    print "good"
                #else:
                #    print "bad"


    def encrypt(self):
        if not self.isLoaded:

            content = ErrorDialog(load=self.cos, cancel=self.dismiss_popup)
            self._popup = Popup(title="File not Loaded!", content=content,
                                size_hint=(0.9, 0.9))
            self._popup.open()
        if self.loaded_file is FILETYPE.WAV :
            content = ErrorDialog(load=self.cos, cancel=self.dismiss_popup)
            self._popup = Popup(title="Only BMP files are supported!", content=content,
                                size_hint=(0.9, 0.9))
            self._popup.open()
        elif self.loaded_file is FILETYPE.BMP:
            file = open(self.h.filename,"rb")
            image = file.read()
            file.close()

            header = image[:54]
            data = image[54:84]
            enc = self.rsaModule.encrypt(np.transpose(np.fromstring(data, dtype=np.uint8)))
            dec = self.rsaModule.decrypt(enc)     
            print(np.fromstring(data, dtype=np.uint8)[0:10])
            print(dec[0:10])
            print(len(dec))
            print(len(data))
            print([ord(c) for c in data[0:10]])
            print(dec[0:10])
            file = open("example2.bmp","wb")
            for i in range(len(dec)):
                if dec[i] > 255:
                    print('RSA error')
                    self.moduleRSA = RSA()
                    return
                        
            d = [int(v) for v in dec]
            d2 = [chr(v) for v  in d]
            print(d2)
            file.write(header.join(d2))
            file.close()
            print("--------------------------------------")

    

    def decrypt(self):
        if not self.isLoaded:

            content = ErrorDialog(load=self.cos, cancel=self.dismiss_popup)
            self._popup = Popup(title="File not Loaded!", content=content,
                                size_hint=(0.9, 0.9))
            self._popup.open()
        if self.loaded_file is FILETYPE.WAV :
            content = ErrorDialog(load=self.cos, cancel=self.dismiss_popup)
            self._popup = Popup(title="Only BMP files are supported!", content=content,
                                size_hint=(0.9, 0.9))
            self._popup.open()
        elif self.loaded_file is FILETYPE.BMP:
            file = open(self.h.filename,"rb")
            image = file.read()
            file.close()
            header = image[:54]
            data = image[54:]
            print(np.fromstring(data, dtype=np.uint8)[0:10])
            #dec = self.rsaModule.decrypt(np.fromstring(data, dtype=np.uint8))
            #file = open("example22.bmp","wb")
            #file.write(header+dec.tobytes())
            #file.close()

            
            #dec = rsaModule.decrypt(enc)
            #if (self.h.data==dec).all:
            #    print "good"
            #else:
            #    print "bad"
class Wavreader(App):
    pass


Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('ErrorDialog', cls=ErrorDialog)


if __name__ == '__main__':
    Wavreader().run()
