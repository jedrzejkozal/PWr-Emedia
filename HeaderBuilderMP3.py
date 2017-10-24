from HeaderBuilder import HeaderBuilder

class HeaderBuilderMP3(HeaderBuilder):
    def __init__(self):
        super(self.__class__, self).__init__()

    def build(self, file):
        #for f in file:
        #    print f

        #f = file.read()
        #print f

        #file.readline()
        return self.header

h = HeaderBuilderMP3()
h.header.add_property("aaa", "b")
h.header.add_property("aax", "c")
print h.readHeader("test2.jpg")
