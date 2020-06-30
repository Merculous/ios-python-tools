import sys
from random import choice, seed
from string import ascii_letters, digits
from urllib.parse import urlsplit

try:
    import progressbar
except ImportError:
    raise

"""

All of the helper functions or just a module to store other functions
that don't have a particular module that its similar to.

Basically just 'tools'.

"""

# Maybe convert progress into my own custom file downloader that auto grabs the data such as filesize, duration, etc.

# https://stackoverflow.com/questions/37748105/how-to-use-progressbar-module-with-urlretrieve

pbar = None


def showProgress(block_num, block_size, total_size):
    global pbar
    if pbar is None:
        pbar = progressbar.ProgressBar(maxval=total_size)
        pbar.start()
    downloaded = block_num * block_size
    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()
        pbar = None


def splitToFileName(path):
    split = urlsplit(path)
    filename = split.path.split('/')[-1]
    return filename


def splitKbag(kbag=str):
    if len(kbag) != 96:
        sys.exit('String provided is not 96 bytes! The length read was:', len(kbag))

    iv = kbag[:32]
    key = kbag[-64:]
    data = {
        'iv': iv,
        'key': key
    }
    return data


def getDeviceType(device):
    for index in range(0, len(device)-3):
        if device[index] in digits:
            return device[:index]
    return False


def getMajorDeviceRevision(device):
    splitting_point = device.find(',')
    for index in range(splitting_point-1, 3, -1):
        if device[index] in ascii_letters:
            return int(device[index+1:splitting_point])
    return -1


def getMinorDeviceRevision(device):
    return int(device[device.find(',')+1:])


def fastTokenHex(byte_length):
    hexdigits = '0123456789abcdef'
    token = ''

    seed()
    for i in range(0, byte_length * 2):
        token += choice(hexdigits)
    return token
