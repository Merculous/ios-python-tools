import os
import sys
import zipfile

import bsdiff4

# TODO Create a write-up to make on how to make these patches manually


class IPSW(object):
    def __init__(self, ipsw):
        super().__init__()

        self.ipsw = ipsw

    def isIPSW(self):
        if zipfile.is_zipfile(self.ipsw):  # ipsw's are just zip archives
            return True
        else:
            return False

    def create24KpwnIPSW(self):  # LLB is patched to enable untethered downgrading without shsh
        if self.isIPSW():
            with zipfile.ZipFile(self.ipsw, 'r') as f:
                if not os.path.exists('IPSW'):
                    os.mkdir('IPSW')
                f.extractall('IPSW')
        else:
            sys.exit(f'{self.ipsw} is not a zip archive!')

    def createPwnageToolIPSW(self):  # Pre-jailbroken ipsw
        pass

    def createOdysseusIPSW(self):  # Patched ipsw to downgrade with blobs or to extract iBoot to dump shsh with generator
        pass

    def createDRAIPSW(self):  # Untethered downgrade and optionally, pre-jailbroken, for use with Dora's fork of iloader
        pass

    # ----------------------------------

    # Below will output the patches into a bundle, readable by ipsw binary from xpwn

    # ----------------------------------

    def create24KpwnBundle(self):
        pass

    def createPwnageToolBundle(self):
        pass

    def createOdysseusBundle(self):
        pass

    def createDRABundle(self):
        pass

    # ----------------------------------
