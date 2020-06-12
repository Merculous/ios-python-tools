#import os
#import sys
#import zipfile

#import bsdiff4

# TODO Create a write-up to make on how to make these patches manually


class IPSW(object):
    def __init__(self, ipsw):
        super().__init__()

        self.ipsw = ipsw
