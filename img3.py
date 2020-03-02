import os
import sys


"""
VERS: iBoot version of the image
SEPO: Security Epoch
SDOM: Security Domain
PROD: Production Mode
CHIP: Chip to be used with. example: 0x8900 for S5L8900.
BORD: Board to be used with
KBAG: Contains the IV and key required to decrypt; encrypted with the GID Key
SHSH: RSA encrypted SHA1 hash of the file
CERT: Certificate
ECID: Exclusive Chip ID unique to every device
TYPE: Type of image, should contain the same string as the header's ident
DATA: Real content of the file
NONC: Nonce used when file was signed.
CEPO: Chip epoch
OVRD:
RAND:
SALT:
"""


class img3(object):
    def __init__(self, file):
        super().__init__()

        self.file = file

    # Data is reversed (little-endian) IMG3 magic will be "3gmI". Need a good way to take a string, convert to hex or whatever, and reverse it.

    def printTags(self):
        with open(self.file, 'rb') as f:
            data = f.read()

            if b'3gmI' in data:
                print('I see a IMG3 tag at index:', hex(data.find(b'3gmI')))

            if b'SREV' in data:
                print('I see a VERS tag at index:', hex(data.find(b'SREV')))

            if b'OPES' in data:
                print('I see a SEPO tag at index:', hex(data.find(b'OPES')))

            if b'MODS' in data:
                print('I see a SDOM tag at index:', hex(data.find(b'MODS')))

            if b'DORP' in data:
                print('I see a PROD tag at index:', hex(data.find(b'DORP')))

            if b'PIHC' in data:
                print('I see a CHIP tag at index:', hex(data.find(b'PIHC')))

            if b'DROB' in data:
                print('I see a BORD tag at index:', hex(data.find(b'DROB')))

            if b'GABK' in data:
                print('I see a KBAG tag at index:', hex(data.find(b'GABK')))

            if b'HSHS' in data:
                print('I see a SHSH tag at index:', hex(data.find(b'HSHS')))

            if b'TREC' in data:
                print('I see a CERT tag at index:', hex(data.find(b'TREC')))

            if b'DICE' in data:
                print('I see a ECID tag at index:', hex(data.find(b'DICE')))

            if b'EPYT' in data:
                print('I see a TYPE tag at index:', hex(data.find(b'EPYT')))

            if b'DTAD' in data:
                print('I see a DATA tag at index:', hex(data.find(b'DTAD')))

            if b'CNON' in data:
                print('I see a NONC tag at index:', hex(data.find(b'CNON')))

            if b'OPEC' in data:
                print('I see a CEPO tag at index:', hex(data.find(b'OPEC')))

            if b'DRVO' in data:
                print('I see a OVRD tag at index:', hex(data.find(b'DRVO')))

            if b'DNAR' in data:
                print('I see a RAND tag at index:', hex(data.find(b'DNAR')))

            if b'TLAS' in data:
                print('I see a SALT tag at index:', hex(data.find(b'TLAS')))

            if b'encrcdsa' in data:
                sys.exit('This is a rootfs!')

        f.close()
