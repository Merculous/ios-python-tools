import os
import plistlib


class Bundle:
    def __init__(self, bundle):
        super().__init__()

        self.bundle = bundle

    def isBundle(self):
        if os.path.isdir(self.bundle):
            # TODO Check for .patch, and Info.plist files
            pass
        else:
            raise ValueError('{} is not a bundle!'.format(self.bundle))
