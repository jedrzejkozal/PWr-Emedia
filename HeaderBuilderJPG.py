from HeaderBuilder import HeaderBuilder

class HeaderBuilderJPG(HeaderBuilder):
    def __init__(self):
        super(self.__class__, self).__init__()

    def read_h(self, file):
        #JPEG SOI marker (FFD8 hex)
        soi = self.read_bytes(file, 2)
        if soi != 0xFFD8:
            raise ValueError('No SOI at begening of the header!')

        #image width in pixels
        img_w = self.read_bytes(file, 2)
        print img_w

        #image height in pixels
        img_h = self.read_bytes(file, 2)
        print img_h

        #number of components (1 = grayscale, 3 = RGB)
        numbComp = self.read_bytes(file, 1)
        print numbComp

        #horizontal/vertical sampling factors for component 1
        sampling_factor = self.read_bytes(file, 1)
        print sampling_factor

    def build(self, file):
        self.read_h(file)

        return self.header

if __name__ == '__main__':
    h = HeaderBuilderJPG()
    h.readHeader("test1.jpg")
    h.printHeader()
