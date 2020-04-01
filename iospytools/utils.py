import json
import os
import sys
import time
import ssl
import platform
import urllib.request
from math import floor
from urllib.parse import urlsplit

import progressbar

"""

All of the helper functions or just a module to store other functions
that don't have a particular module that its similar to.

Basically just 'tools'.

"""

# Maybe convert progress into my own custom file downloader that auto grabs the data such as filesize, duration, etc.

# https://stackoverflow.com/questions/37748105/how-to-use-progressbar-module-with-urlretrieve

pbar = None

def show_progress(block_num, block_size, total_size):
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


def downloadJSONData(url, filename):
    if platform.system() == 'Windows': # I don't see any ssl certficate like in MacOS for Windows
        if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
            ssl._create_default_https_context = ssl._create_unverified_context
        
    request = urllib.request.urlopen(url).read()
    convert = json.loads(request)
    with open(f'{filename}.json', 'w') as file:
        json.dump(convert, file, indent=4)
    file.close()


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


def clean():
    for file in os.listdir(os.getcwd()):
        if file.endswith('json'):
            os.remove(file)
        elif file.endswith('plist'):
            os.remove(file)
