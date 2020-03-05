import os
import re
import struct
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
OVRD: Overide thingy for demotion - axi0mX
RAND:
SALT:
"""


class img3(object):
    def __init__(self, file):
        super().__init__()

        self.file = file

    # Data is reversed (little-endian) IMG3 magic will be "3gmI". Need a good way to take a string, convert to hex or whatever, and reverse it.

    def parseImage(self):
        with open(self.file, 'rb') as f:
            data = f.read()

            if b'3gmI' in data:
                print('I see a IMG3 tag at index:', hex(data.find(b'3gmI')))

            if b'SREV' in data:
                print('I see a VERS tag at index:', hex(data.find(b'SREV')))
                ibootstring = re.findall(r"iBoot-([0-9.]*[~0-9]+)", str(data))  # regex check for numbers, and periods
                ibootversion = f'iBoot-{ibootstring[0]}'
                print(f'Found {ibootversion} at index:', hex(data.find(bytes(ibootversion, 'utf-8'))))

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
                offset = data.find(b'EPYT')
                print('I see a TYPE tag at index:', hex(offset))

                if b'lnrk' in data:  # TODO
                    print('\nI see a krnl tag at index:', hex(data.find(b'lnrk')))
                    print('The file is a kernel!')

                # TODO Some mach-o parsing, print the other stuff

                # if b'__TEXT' in data:  # TODO
                #print('Found __TEXT at index:', hex(data.find(b'__TEXT')))

                if b'ksdr' in data:
                    print('\nI see a rdsk tag at index:', hex(data.find(b'ksdr')))
                    print('The file is a ramdisk!')

                if b'ssbi' in data:
                    print('\nI see a ibss tag at index:', hex(data.find(b'ssbi')))
                    print('The file is a ibss!')

                if b'cebi' in data:
                    print('\nI see a ibec tag at index:', hex(data.find(b'cebi')))
                    print('The file is a ibec!')

                if b'tobi' in data:
                    print('\nI see a ibot tag at index:', hex(data.find(b'tobi')))
                    print('The file is a iboot!')

                if b'blli' in data:
                    print('\nI see a illb tag at index:', hex(data.find(b'blli')))
                    print('The file is a llb!')

                if b'ertd' in data:
                    print('\nI see a dtre tag at index:', hex(data.find(b'ertd')))
                    print('The file is a devicetree!')

                if b'ogol' in data:
                    print('\nI see a logo tag at index:', hex(data.find(b'ogol')))
                    print('The file is a applelogo!')

                if b'0ghc' in data:
                    print('\nI see a chg0 tag at index:', hex(data.find(b'0ghc')))
                    print('The file is a batterycharging0!')

                if b'1ghc' in data:
                    print('\nI see a chg1 tag at index:', hex(data.find(b'1ghc')))
                    print('The file is a batterycharging1!')

                if b'Ftab' in data:
                    print('\nI see a batF tag at index:', hex(data.find(b'Ftab')))
                    print('The file is a batteryfull!')

                if b'0tab' in data:
                    print('\nI see a bat0 tag at index:', hex(data.find(b'0tab')))
                    print('The file is a batterylow0!')

                if b'1tab' in data:
                    print('\nI see a bat1 tag at index:', hex(data.find(b'1tab')))
                    print('The file is a batterylow1!')

                if b'Cylg' in data:
                    print('\nI see a glyC tag at index:', hex(data.find(b'Cylg')))
                    print('The file is a glyphcharging!')

                if b'Pylg' in data:
                    print('\nI see a glyP tag at index:', hex(data.find(b'Pylg')))
                    print('The file is a glyphplugin!')

                if b'vrsn' in data:
                    print('\nI see a nsrv tag at index:', hex(data.find(b'vrsn')))
                    print('The file is a needservice!')

                if b'mcer' in data:
                    print('\nI see a recm tag at index:', hex(data.find(b'mcer')))
                    print('The file is a recoverymode!')

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
                print('I see a encrcdsa tag at index:', hex(data.find(b'encrcdsa')))
                print('The file is a rootfs!')

        f.close()
