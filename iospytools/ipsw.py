import os
import zipfile

try:
    # from .bundle import Bundle
    from .manifest import BuildManifest
except ImportError:
    raise

# TODO Create a write-up to make on how to make these patches manually


class IPSW(object):
    def __init__(self, ipsw):
        super().__init__()

        try:
            zipfile.is_zipfile(ipsw)
        except ValueError:
            print('{} is not a zip archive!'.format(ipsw))
            raise
        else:
            self.ipsw = ipsw

    def parse(self):
        with zipfile.ZipFile(self.ipsw, 'r') as f:
            f.extract('BuildManifest.plist')
            data = BuildManifest()
            stuff = data.extractData()
            os.remove('BuildManifest.plist')
            return stuff
