from Header import Header

class HeaderBuilder(object):
    def __init__(self):
        self.header = Header()

    def readHeader(self, filename):
        f = open(filename, 'r')
        self.build(f)
        f.close()
        return self.header

    def printHeader(self):
        for prop in self.header.map:
            print prop

    def build(self, filename):
        return self.header
