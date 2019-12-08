import json
import os
from urllib.request import urlretrieve, urlopen
from zipfile import ZipFile, is_zipfile
from io import BytesIO

import utils


# Another thing, parse version data, and if its already a buildid, then use that, otherwise, convert.
# This will be added in a bit. I'm guessing I need some RegEx to handle this?

def linksForDevice(device):
    url = f'https://api.ipsw.me/v4/device/{device}?type=ipsw'
    utils.downloadJSONData(url, device)


def downloadIPSW(device, version):
    buildid = utils.iOSToBuildid(device, version)
    linksForDevice(device)
    with open(f'{device}.json', 'r') as file:
        data = json.load(file)
        i = 0
        buildidFromJsonFile = data['firmwares'][i]['buildid']
        while buildidFromJsonFile != buildid:
            i += 1
            buildidFromJsonFile = data['firmwares'][i]['buildid']

        url = data['firmwares'][i]['url']
        ios = data['firmwares'][i]['version']
        filename = utils.splitToFileName(url)

        print(f'Device: {device}')
        print(f'iOS: {ios}')
        print(f'Buildid: {buildidFromJsonFile}')
        print(f'Filename: {filename}')
        urlretrieve(url, filename, utils.progress)
        print('\n')
        file.close()
        os.remove(f'{device}.json')


def signed(device):
    linksForDevice(device)
    with open(f'{device}.json', 'r') as file:
        data = json.load(file)
        print(f'{device} has the following version(s) signed:')
        for stuff in data['firmwares']:
            ios = stuff['version']
            buildid = stuff['buildid']
            sig = stuff['signed']
            lolarray = [ios, buildid, sig]
            if lolarray[2]:
                print(f'{ios} {buildid}')

    file.close()
    os.remove(f'{device}.json')


def downloadBuildManifest(device, version):
    buildid = utils.iOSToBuildid(device, version)
    linksForDevice(device)
    with open(f'{device}.json', 'r') as file:
        data = json.load(file)
        i = 0
        buildidFromJsonFile = data['firmwares'][i]['buildid']
        while buildidFromJsonFile != buildid:
            i += 1
            buildidFromJsonFile = data['firmwares'][i]['buildid']

        url = data['firmwares'][i]['url']
        filename = utils.splitToFileName(url)

        # Start the process of reading and extracting a file from a url
