import os
import plistlib

try:
    import bsdiff4
except ImportError:
    raise


class Bundle:
    def __init__(self, bundle: str):
        super().__init__()

        self.bundle = bundle

    def checkBundle(self):
        try:
            os.path.isdir(self.bundle)
        except ValueError:
            print('{} is not a bundle!'.format(self.bundle))
            raise

    def parsePlist(self):
        with open('{}/Info.plist'.format(self.bundle), 'rb') as f:
            data = plistlib.load(f)
            return data

    def patch(self, path: str, patchfile: str):
        print('Patching: {}'.format(path))
        bsdiff4.file_patch(path, '{}.patched'.format(
            os.path.basename(path)), patchfile)
