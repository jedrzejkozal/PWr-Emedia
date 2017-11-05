from HeaderBuilder import HeaderBuilder

class HeaderBuilderWAV(HeaderBuilder):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.PCM = False

    def read_descriptor(self, file):
        #riff  - endianess big
        riff = self.read_bytes(file, 4)
        #0x52494646 - RIFF in hexadecimal
        if riff != 0x52494646:
            raise ValueError('No RIFF in descriptor chunk.')

        #ChunkSize - endianess little
        #4 + (8 + SubChunk1Size) + (8 + SubChunk2Size)
        chunkSize = self.read_bytes(file, 4, True)
        #SubChunk2Size = SubChunk2Size - 36
        self.header.add_property('ChunkSize', chunkSize)

        #Format: WAVE - endianess big
        wave = self.read_bytes(file, 4)
        #0x52494646 - WAVE in hexadecimal
        if wave != 0x57415645:
            raise ValueError('No WAVE in descriptor chunk.')

    def read_fmt_subchunk(self, file):
        #Subchunk1ID  - endianess big
        fmt = self.read_bytes(file, 4)
        #0x666d7420 - fmt in hexadecimal
        if fmt != 0x666d7420:
            raise ValueError('No fmt in fmt chunk.')

        #Subchunk1Size - endianess little
        SubChunk1Size = self.read_bytes(file, 4, True)
        self.header.add_property('SubChunk1Size', SubChunk1Size)
        if SubChunk1Size == 16:
            self.PCM = True
        else:
            self.PCM = False

        #AudioFormat  - endianess little
        audioFormat = self.read_bytes(file, 2, True)
        if self.PCM and audioFormat != 1:
            print audioFormat
            raise ValueError('AudioFormat not equal to 1, while PCM')
        else:
            self.header.add_property('AudioFormat', audioFormat)

        #NumChannels  - endianess little
        numChannels = self.read_bytes(file, 2, True)
        self.header.add_property('NumChannels', numChannels)

        #SampleRate  - endianess little
        sampleRate = self.read_bytes(file, 4, True)
        self.header.add_property('SampleRate', sampleRate)

        #ButeRate  - endianess little
        byteRate = self.read_bytes(file, 4, True)
        self.header.add_property('ByteRate', byteRate)

        #BlockAlign  - endianess little
        blockAlign = self.read_bytes(file, 2, True)
        self.header.add_property('BlockAlign', blockAlign)

        #BitsPerSample  - endianess little
        bitsPerSample = self.read_bytes(file, 2, True)
        self.header.add_property('BitsPerSample', bitsPerSample)

        #adctional validation:
        if byteRate != sampleRate * numChannels * bitsPerSample/8:
            raise ValueError('ByteRate != SampleRate * NumChannels * BitsPerSample/8')

        if blockAlign != numChannels * bitsPerSample/8:
            raise ValueError('BlockAlign != NumChannels * BitsPerSample/8')

        if not self.PCM:
            extraParamSize = self.read_bytes(file, 2)
            if SubChunk1Size - 16 != extraParamSize:
                raise ValueError('BlockAlign != NumChannels * BitsPerSample/8')
            else:
                self.header.add_property('ExtraParamSize', extraParamSize)

                extraParams = self.read_bytes(file, extraParamSize)
                self.header.add_property('ExtraParams', extraParams)

    def read_data_subchunk(self, file):
        #Subchunk2ID  - endianess big
        data = self.read_bytes(file, 4)
        #0x64617461 - data in hexadecimal
        if data != 0x64617461:
            raise ValueError('No data in data chunk.')

        #Subchunk2Size - endianess little
        subchunk2Size = self.read_bytes(file, 4, True)
        self.header.add_property('SubChunk2Size', subchunk2Size)
        if self.header.get_property('ChunkSize') != 36 + (8+self.header.get_property('SubChunk1Size')) + (8+subchunk2Size):
            print 'there are some bytes after data chunk'
            print 'ChunkSize = %d' % self.header.get_property('ChunkSize')
            print 'SubChunk1Size = %d' % self.header.get_property('SubChunk1Size')
            print 'SubChunk2Size = %d' % subchunk2Size
            print

        #actual data - endianess little
        self.data = bytearray(file.read(self.header.get_property('SubChunk2Size')))
        #self.data = bytearray(file.read())
        #self.data = self.data[::-1]

        #print file.read()

    def build(self, file):
        self.read_descriptor(file)
        self.read_fmt_subchunk(file)
        data = self.read_data_subchunk(file)

        return self.header, self.data

if __name__ == '__main__':
    h = HeaderBuilderWAV()
    h.readHeader("test3.wav")
    h.printHeader()
