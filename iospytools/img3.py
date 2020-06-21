# import struct
# import sys
import os
# import math
import humanize

"""
typedef struct img3File {
    uint32_t magic;       // ASCII_LE("Img3")
    uint32_t fullSize;    // full size of fw image
    uint32_t sizeNoPack;  // size of fw image without header
    uint32_t sigCheckArea;// although that is just my name for it, this is the
                          // size of the start of the data section (the code) up to
                          // the start of the RSA signature (SHSH section)
    uint32_t ident;       // identifier of image, used when bootrom is parsing images
                          // list to find LLB (illb), LLB parsing it to find iBoot (ibot),
                          // etc.
    img3Tag  tags[];      // continues until end of file
};

typedef struct img3Tag {
    uint32_t magic;            // see below
    uint32_t totalLength;      // length of tag including "magic" and these two length values
    uint32_t dataLength;       // length of tag data
    uint8_t  data[dataLength];
    uint8_t  pad[totalLength - dataLength - 12]; // Typically padded to 4 byte multiple
};


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
OVRD: Override thingy for demotion - axi0mX
RAND:
SALT:
"""


class IMG3(object):
    def __init__(self, file):
        super().__init__()

        self.file = file
        self.totalsize = os.path.getsize(self.file)
        print('Name: {}'.format(os.path.basename(self.file)))
        print('Size: {}'.format(humanize.naturalsize(self.totalsize)))

        """

        Class to parse and interact with Apple's img3 formatted files.

        """

    def parseImage(self):
        # Return tags, iBoot version, and other info about an img3

        # Can return a dict with tags and their position, maybe even make this somewhat of a new way of parsing img3?
        # info = {
        #
        # }

        with open(self.file, 'rb') as f:
            img3_start = f.read(4)
            new = img3_start.decode('utf-8')[::-1]
            if new == 'Img3':
                # To grab proper tag type, we must not only get the type tag, which will give the correct tag, ident will also give the same value
                # which means, we have two sources. So, we should not base the file off of one, to increase likelihood that whatever is parsed is done
                # with as much precision as possible. At least from my point of view, that seems reasonable enough, because with built iBoot however...

                # Get type of img3

                tags = ['rdsk', 'ibss', 'ibec', 'ibot', 'illb', 'dtre', 'logo', 'chg0',
                        'chg1', 'batF', 'bat0', 'bat1', 'glyC', 'glyP', 'nsrv', 'recm']

                # data = struct.unpack('<I', f.read())
                # print(type(data))
                data = f.read()

                for tag in tags:
                    # Convert to bytes, and reverse the bytes due to little-endian
                    tag = tag.encode()[::-1]
                    count = 1
                    duplicated = list()
                    if tag in data:
                        count += 1
                        duplicated.append(tag)
                        duplicated.append(count)

                    print('Tag {} repeated {} times!'.format(
                        duplicated[0], duplicated[1]))

            else:
                raise ValueError('Not an img3 file')
