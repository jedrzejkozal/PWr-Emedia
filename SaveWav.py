from HeaderBuilderWAV import *

class SaveWAV:
    def __init__(self, header, data):
        self.header = header
        self.data = data

        if header.get_property('SubChunk1Size') == 16:
            self.PCM = True
        else:
            self.PCM = False

    def to_bytes(self, n, length):
        bytes = bytearray()
        for i in reversed(range(length)):
            bytes.append((n >> i*8) & 0xff)
        return bytes

    def hex_to_bytearray(self, hex, length, littleEndian=False):
        b = self.to_bytes(hex, length)
        if littleEndian:
            b = b[::-1]
        return b

    def write_prop(self, file, name, size, littleEndian=False):
        file.write(self.hex_to_bytearray(self.header.get_property(name),size, littleEndian))

    def write_descriptor(self, file):
        file.write('RIFF')
        self.write_prop(file, 'ChunkSize', 4, True)
        file.write('WAVE')

    def write_fmt(self, file):
        file.write('fmt ')
        self.write_prop(file, 'SubChunk1Size', 4, True)
        self.write_prop(file, 'AudioFormat', 2, True)
        self.write_prop(file, 'NumChannels', 2, True)
        self.write_prop(file, 'SampleRate', 4, True)
        self.write_prop(file, 'ByteRate', 4, True)
        self.write_prop(file, 'BlockAlign', 2, True)
        self.write_prop(file, 'BitsPerSample', 2, True)

        if not self.PCM:
            self.write_prop(file, 'ExtraParamSize', 2, True)
            self.write_prop(file, 'ExtraParams', self.header.get_property('ExtraParamSize'), True)

    def write_data(self, file):
        file.write('data')
        file.write(self.data)

    def write(self, file):
        self.write_descriptor(file)
        self.write_fmt(file)
        self.write_data(file)

        return True

    def save(self, filename):
        f = open(filename, 'w')
        f.truncate()
        self.write(f)
        f.close()

if __name__ == '__main__':
    h = HeaderBuilderWAV()
    h.readHeader("test3.wav")
    #h.readHeader("gardenss_48KHz.wav")
    h.printHeader()

    s = SaveWAV(h.header, h.data)
    s.save('result.wav')
    print
    s.header.printHeader()
    print

    h1 = HeaderBuilderWAV()
    h1.readHeader('result.wav')
