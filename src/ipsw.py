import os
import plistlib
import shutil
from zipfile import is_zipfile, ZipFile


class Manifest(object):
    def __init__(self, manifest: bytes):
        super().__init__()

        self.manifest = plistlib.loads(manifest)

    def getInfo(self):
        info = {
            'device': self.manifest['SupportedProductTypes'][0],
            'ios': self.manifest['ProductVersion'],
            'buildid': self.manifest['ProductBuildVersion'],
            'chipid': self.manifest['BuildIdentities'][0]['ApChipID'],
            'codename': self.manifest['BuildIdentities'][0]['Info']['BuildTrain'],
            'deviceclass': self.manifest['BuildIdentities'][0]['Info']['DeviceClass'],
            'paths': list()
        }

        for path in self.manifest['BuildIdentities'][0]['Manifest'].items():
            name = path[0]
            filepath = path[1]['Info']['Path']
            info['paths'].append({name: filepath})

        return info


class IPSW(object):
    def __init__(self, ipsw):
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
