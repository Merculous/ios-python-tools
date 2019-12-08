import tempfile
import zipfile
import sys
import json
import os
import time
from math import floor
from urllib.parse import urlsplit
from urllib.request import urlopen, Request

import ipswapi

"""
def tss_request_manifest(board, build, ecid, cpid=None, bdid=None):
    url = 'http://api.ineal.me/tss/manifest/%s/%s' % (board, build)
    r = requests.get(url, headers={'User-Agent': USER_AGENT})
    return r.text.replace('<string>$ECID$</string>', '<integer>%s</integer>' % (ecid))

def request_blobs_from_apple(board, build, ecid, cpid=None, bdid=None):
    url = 'http://gs.apple.com/TSS/controller?action=2'
    r = requests.post(url, headers={'User-Agent': USER_AGENT}, data=tss_request_manifest(board, build, ecid, cpid, bdid))
"""


def grabManifest():
    pass


def saveblobs(ecid, device):
    ipswapi.linksForDevice(device)
    with open(f'{device}.json') as file:
        data = json.load(file)
        for stuff in data['firmwares']:
            ios = stuff['version']
            sig = stuff['signed']
            lolarray = [ios, sig]
            if lolarray[1]:
                print(f'Saving blobs for iOS: {ios}')
                # url = 'http://gs.apple.com/TSS/controller?action=2'
                # req = Request(url, data=tss_request_manifest(board, build, ecid, cpid, bdid))
            else:
                continue

    file.close()
    os.remove(f'{device}.json')


def progress(count, block_size, total_size):  # Check README for credit (not mine)
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
    ipswapi.linksForDevice(device)
    with open(f'{device}.json', 'r') as file:
        data = json.load(file)
        i = 0
        iOSFromJsonFile = data['firmwares'][i]['version']
        while iOSFromJsonFile != iOS:
            i += 1
            iOSFromJsonFile = data['firmwares'][i]['version']

        buildid = data['firmwares'][i]['buildid']

    file.close()
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
