import tempfile
import zipfile
import sys
import json
import os
import time
from math import floor
from urllib.parse import urlsplit
from urllib.request import urlopen

import api


# This will help with parsing every file within an ipsw that has keys. Should print every file and their keys.
def keyHelper():
    pass


def progress(count, block_size, total_size):  # Check README for credit
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration))
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write(
        f'\r{percent}%, {floor(progress_size / (1024 * 1024))} MB, {speed} KB/s, {floor(duration)} seconds passed')
    sys.stdout.flush()


def downloadJSONData(url, filename):
    json_data = urlopen(url).read()
    data = json.loads(json_data)
    with open(f'{filename}.json', 'w') as write_file:
        json.dump(data, write_file, indent=4)


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


def splitToFileName(path):
    split = urlsplit(path)
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