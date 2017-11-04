from HeaderBuilder import HeaderBuilder

class HeaderBuilderWAV(HeaderBuilder):
    def __init__(self):
        super(self.__class__, self).__init__()

    def build(self, file):
        #for f in file:
        #    print f

        #f = file.read()
        #print f

        #l = file.readline()
        #print l

        riff = file.read(4)
        if riff != 0x52494646: #0x52494646 - hexadecimal begining of the file
            raise ValueError('No RIFF at begining of file.')
        print riff

        byte = file.read(1)
        print byte
        byte = file.read(1)
        print byte
        byte = file.read(1)
        print byte
        byte = file.read(1)
        print byte

        return self.header

if __name__ == '__main__':
    h = HeaderBuilderWAV()
    #h.header.add_property("aaa", "b")
    #h.header.add_property("aax", "c")
    h.readHeader("test3.wav")
    h.printHeader()
