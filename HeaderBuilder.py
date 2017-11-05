from Header import Header

class HeaderBuilder(object):
    def __init__(self):
        self.header = Header()

    def bytearray_to_hex(self, array):
        h = 0
        for i in range(len(array)):
            h = (h << 8) + int(array[i])
        return h

    def read_bytes(self, file, n, littleEndian=False):
        bc = bytearray(file.read(n))
        if littleEndian:
            bc = bc[::-1]
        return self.bytearray_to_hex(bc)

    def readHeader(self, filename):
        f = open(filename, 'r')
        self.build(f)
        f.close()
        return self.header

    def printHeader(self):
        self.header.printHeader()

    def build(self, filename):
        return self.header
