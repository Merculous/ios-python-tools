import tempfile
import zipfile
import sys
import json
import os
from urllib.parse import urlsplit

import api


# Hopefully this fixes the issue where if an iOS has two different buildid's, it should just download the first?
def iOSToBuildid(device, iOS):
    api.linksForDevice(device)  # Get the json file
    with open(f'{device}.json', 'r') as file:
        data = json.load(file)
        i = 0
        iOSFromJsonFile = data['firmwares'][i]['version']
        while iOSFromJsonFile != iOS:
            i += 1
            iOSFromJsonFile = data['firmwares'][i]['version']

        buildid = data['firmwares'][i]['buildid']
        os.remove(f'{device}.json')
        return buildid


def splitIPSWUrlToName(url):
    split = urlsplit(url)
    filename = split.path.split('/')[-1]
    return filename


def extractIPSW(file):
    if zipfile.is_zipfile(file):
        tmp = tempfile.mkdtemp()  # Make temp dir
        print(f'We are using {tmp} as the temp dir')
        with zipfile.ZipFile(file, 'r') as ipsw:
            ipsw.extractall(tmp)
    else:
        print(f'{file} is not a zip archive')


def splitKbag(str):
    size = len(str)
    if size != 96:
        print(f'Length: {size}')
        sys.exit('String provided is not 96 bytes!')
    else:
        # TODO I know for sure this can be made better. Maybe?
        iv = str[:32]
        key = str[-64:]
        print(f'IV: {iv}')
        print(f'Key: {key}')
