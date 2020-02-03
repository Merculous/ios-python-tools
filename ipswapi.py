import json
import os
from urllib.request import urlretrieve

import utils


"""

This is mainly the heart of the script.

Handles data from ipsw.me api

"""


def linksForDevice(device):
    url = f'https://api.ipsw.me/v4/device/{device}?type=ipsw'
    return utils.downloadJSONData(url, device)


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


def signed(device):
    signedVersions = []
    linksForDevice(device)
    with open(f'{device}.json', 'r') as file:
        data = json.load(file)
        for stuff in data['firmwares']:
            ios = stuff['version']
            buildid = stuff['buildid']
            signed = stuff['signed']
            if signed:
                version = [ios, buildid]
                signedVersions.append(version)

    file.close()
    return signedVersions

