from HeaderBuilder import HeaderBuilder
from scipy import fftpack, ndimage
from PIL import Image
import numpy as np

class HeaderBuilderBMP(HeaderBuilder):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.data = ''

    def read_h(self, file):
        #signature, must be 4D42 hex
        signature = self.read_bytes(file, 2, True)
        if signature != 0x4D42:
            raise ValueError('No SOI at begening of the header!')

        #size of BMP file in bytes (unreliable)
        file_size = self.read_bytes(file, 4, True)
        #print file_size
        self.header.add_property('FileSize', file_size)

        #reserved
        zeros = self.read_bytes(file, 4, True)
        if zeros != 0x00:
            raise ValueError('Reserved bits are not equal to zero')

        #offset to start of image data in bytes
        offset = self.read_bytes(file, 4, True)
        #print offset
        self.header.add_property('Offset', offset)

        #size of BITMAPINFOHEADER structure, must be 40
        header_size = self.read_bytes(file, 4, True)
        if header_size != 40:
            raise ValueError('size of BITMAPINFOHEADER structure not equal to 40')

        #image width in pixels
        img_w = self.read_bytes(file, 4, True)
        self.header.add_property('ImageWidth', img_w)

        #image height in pixels
        img_h = self.read_bytes(file, 4, True)
        self.header.add_property('ImageHeight', img_h)

        #number of planes in the image, must be 1
        numb_of_planes = self.read_bytes(file, 2, True)
        if numb_of_planes != 1:
            raise ValueError('number of planes in image not equal to 1')
        else:
            self.header.add_property('NumberOfPlains', numb_of_planes)

        #number of bits per pixel (1, 4, 8, 24, or 32)
        bits_per_pixel = self.read_bytes(file, 2, True)
        if bits_per_pixel != 1  and  bits_per_pixel != 4  and  \
           bits_per_pixel != 8  and  bits_per_pixel != 24 and  \
           bits_per_pixel != 32:
           raise ValueError('number of bits per pixel not eq 1, 4, 8, 24 or 32')
        else:
            self.header.add_property('BitsPerPixel', bits_per_pixel)


        #compression type (0=none, 1=RLE-8, 2=RLE-4)
        compr_type = self.read_bytes(file, 4, True)
        if compr_type != 0 and compr_type != 1 and compr_type != 2:
            raise ValueError('compression type has unnknown value')
        else:
            self.header.add_property('CompressionType', compr_type)

        #size of image data in bytes (including padding)
        img_size = self.read_bytes(file, 4, True)
        self.header.add_property('ImgageSizeWithPadding', img_size)

        #horizontal resolution in pixels per meter (unreliable)
        hor_res = self.read_bytes(file, 4, True)
        self.header.add_property('HorizontalResolution', hor_res)

        #vertical resolution in pixels per meter (unreliable)
        ver_res = self.read_bytes(file, 4, True)
        self.header.add_property('VerticalResolution', ver_res)

        #number of colors in image, or zero
        colors = self.read_bytes(file, 4, True)
        self.header.add_property('NumberOfColors', colors)

        #number of important colors, or zero
        important_colors = self.read_bytes(file, 4, True)
        self.header.add_property('NumberOfImportantColors', important_colors)

    def build(self, file):
        self.read_h(file)

        img = Image.open(self.filename).convert('L')
        self.data = np.asarray(img.getdata()).reshape(img.size)
        return self.header, self.data

if __name__ == '__main__':
    h = HeaderBuilderBMP()
    h.readHeader("test4.bmp")
    #h.readHeader("test5.bmp")
    h.printHeader()
