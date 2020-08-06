import struct

'''

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

'''

'''

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
OVRD: For demoting -axi0mX
RAND:
SALT: For flavor -axi0mX (lmao)

'''

'''

Decryption is done using the modulus at cert + 0xA15
0xC to SHSH is SHAed

'''


class IMG3:
    def __init__(self, file):
        super().__init__()

        with open(file, 'rb') as f:
            self.data = f.read()
            self.info = {
                'magic': struct.unpack('4s', self.data[0:4])[0][::-1].decode(),
                'size': struct.unpack('I', self.data[4:8])[0],
                'unpacksize': struct.unpack('I', self.data[8:12])[0],
                'sigcheckarea': struct.unpack('I', self.data[12:16])[0],
                'ident': struct.unpack('4s', self.data[16:20])[0][::-1].decode(),
                'tags': None,
                'kbag': None,
                'version': None
            }

            # Add tag values

            tags = list()

            i = 20

            while i < 20 + self.info['unpacksize']:
                self.tag_info = {
                    'magic': struct.unpack('4s', self.data[i:i+4])[0][::-1].decode(),
                    'totalsize': struct.unpack('I', self.data[i+4:i+8])[0],
                    'datasize': struct.unpack('I', self.data[i+8:i+12])[0],
                    'data': None
                }

                tag_size = self.tag_info['totalsize']
                self.tag_info['data'] = self.data[i+12:i+tag_size]

                tags.append(self.tag_info)
                self.info['tags'] = tags

                # Done with tag, move on to next

                i += tag_size

            # Add iBoot version string, if iBoot, of course

            for version in self.info['tags']:
                if version['magic'] == 'VERS':
                    version_info = {
                        'stringsize': struct.unpack('I', version['data'][:4])[0],
                        'string': None
                    }
                    size = version_info['stringsize']
                    version_info['string'] = struct.unpack(
                        '{}s'.format(size), version['data'][4:4+size])[0].decode()
                    self.info['version'] = version_info

            # Add kbag values

            kbags = list()
            for kbag in self.info['tags']:
                if kbag['magic'] == 'KBAG':
                    kbag_info = {
                        'type': struct.unpack('I', kbag['data'][:4])[0],
                        'aes_type': struct.unpack('I', kbag['data'][4:8])[0],
                        'kbag': kbag['data'][8:56].hex()
                    }
                    kbags.append(kbag_info)
            self.info['kbag'] = kbags

            # Add SHSH values

            for blob in self.info['tags']:
                if blob['magic'] == 'SHSH':
                    pass

            # Add CERT values

            for cert in self.info['tags']:
                if cert['magic'] == 'CERT':
                    pass

    def printInfo(self):
        return self.info

    def printTags(self):
        return self.info['tags']

    def getKBAGS(self):
        return self.info['kbag']
