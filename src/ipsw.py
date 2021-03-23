import os
import shutil
from zipfile import is_zipfile, ZipFile

from .manifest import Manifest


class IPSW:
    def __init__(self, ipsw: str):
        try:
            is_zipfile(ipsw)
        except OSError:
            print(f'{ipsw} is not a zip file!')
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
