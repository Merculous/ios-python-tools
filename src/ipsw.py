import os
import shutil
from zipfile import is_zipfile, ZipFile

from .manifest import Manifest


class IPSW(object):
    def __init__(self, ipsw: str):
        super().__init__()

        try:
            is_zipfile(ipsw)
        except OSError:
            print('{} is not a zip file!'.format(ipsw))
            raise
        else:
            self.ipsw = ipsw

    def getInfo(self):
        with ZipFile(self.ipsw) as f:
            data = Manifest(f.read('BuildManifest.plist'))
            return data.getInfo()

    def extract(self):
        path = '.ipsw'
        if os.path.exists(path):
            shutil.rmtree(path)  # Delete any previous data, for sanity

        os.mkdir(path)

        with ZipFile(self.ipsw) as f:
            f.extractall(path)
