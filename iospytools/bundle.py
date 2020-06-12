import os
import plistlib

try:
    import bsdiff4
except:
    raise ImportError


class Bundle:
    def __init__(self, bundle):
        super().__init__()

        self.bundle = bundle

    def checkBundle(self):
        if os.path.isdir(self.bundle):
            # TODO Check for .patch, and Info.plist files
            if 'Info.plist' in os.listdir(self.bundle):
                # Check if .patch files exist, check if they are actual patch files
                pass
            else:
                raise FileNotFoundError(
                    'Info.plist must be needed to patch an ipsw!')
        else:
            raise ValueError('{} is not a bundle!'.format(self.bundle))

    def parsePlist(self):
        try:
            path = self.bundle + '/Info.plist'
        except FileNotFoundError:
            print('Oof, Info.plist does not exist!')

        with open(path, 'rb') as f:
            data = plistlib.load(f)
            print(data)
