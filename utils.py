import sys
import json
import os
import time
import xml.etree.ElementTree as ET
from math import floor
from urllib.parse import urlsplit
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile

from remotezip import RemoteZip

import ipswapi

"""

All of the helper functions or just a module to store other functions
that don't have a particular module that its similar to.

Basically just 'tools'.

"""


def saveblobs(device, ecid):
    signed = ipswapi.signed(device)
    url = 'http://gs.apple.com/TSS/controller?action=2'
    for version, buildid in signed:
        downloadBuildManifest(device, version)

        # Parse xml data I guess and add the stuff below

        #with open(f'BuildManifest_{device}_{version}_{buildid}.plist', 'r') as manifest:
            #tree = ET.parse(manifest)
            #root = tree.getroot()[0][0]  # BuildIdentities

        #manifest.close()

    # plist -> dict -> BuildIdentities -> array -> dict -> add the stuff below
    # <key>ApECID</key>
    # <string>ecid</string>

# Maybe convert progress into my own custom file downloader that auto grabs the data such as filesize, duration, etc.


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
    with open(f'{filename}.json', 'w') as file:
        json.dump(data, file, indent=4)

    file.close()


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


def splitKbag(kbag):
    if len(kbag) != 96:
        sys.exit(f'String provided is not 96 bytes! The length read was {len(kbag)}.')
    else:
        iv = kbag[:32]
        key = kbag[-64:]
        return iv, key

def downloadBuildManifest(device, version):
    buildid = iOSToBuildid(device, version)
    ipswapi.linksForDevice(device)

    with open(f'{device}.json', 'r') as file:
        data = json.load(file)
        i = 0
        buildidFromJsonFile = data['firmwares'][i]['buildid']
        while buildidFromJsonFile != buildid:
            i += 1
            buildidFromJsonFile = data['firmwares'][i]['buildid']

        url = data['firmwares'][i]['url']
        manifest = 'BuildManifest.plist'

        # Start the process of reading and extracting a file from a url

        print(f'Downloading manifest for {version}, {buildid}')
        zip = RemoteZip(url)
        zip.extract(manifest)
        os.rename(manifest, f'BuildManifest_{device}_{version}_{buildid}.plist')  # This can be done better
        print('Done downloading!')
        zip.close()

    file.close()
    os.remove(f'{device}.json')
