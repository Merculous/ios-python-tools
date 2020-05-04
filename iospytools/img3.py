import re


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
OVRD: Overide thingy for demotion - axi0mX
RAND:
SALT:
"""


class IMG3(object):
    def __init__(self, file):
        super().__init__()

        self.file = file

        """

        Class to parse and interact with Apple's img3 formatted files.

        """

    # Data is reversed (little-endian) IMG3 magic will be "3gmI". Need a good way to take a string, convert to hex or whatever, and reverse it.

    def parseImage(self):
        # Return tags, iBoot version, and other info about an img3

        info = {

        }

        with open(self.file, 'rb') as f:
            data = f.read()
            print(data)
        f.close()
