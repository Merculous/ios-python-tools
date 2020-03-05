import os
import sys


class img4(object):
    def __init__(self, file):
        super().__init__()

        self.file = file

    def printTags(self):
        with open(self.file, 'rb') as f:
            data = f.read()

            if b'IM4P' in data:
                print('I see a IM4P tag at index:', hex(data.find(b'IM4P')))

        f.close()
