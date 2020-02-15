import os
import sys


class Img3(object):
    def __init__(self, file):
        super().__init__()

        self.file = file
    # Data is reversed (little-endian) IMG3 magic will be "3gmI". Need a good way to take a string, convert to hex or whatever, and reverse it.

    def convertAndReverse(self, string):
        pass

    def printTagMagic(self, file):
        try:
            with open(self.file, 'rb') as f:
                # Data comes out like b'\x01\n' (list[Bytes])
                data = f.readlines()
                # This is actual the first few bytes of the file anyways (at least from my LLB)
                data.index(b'\x49\x6D\x67\x33')
            f.close()
            return data
        except OSError:
            print('Error handling image!')
