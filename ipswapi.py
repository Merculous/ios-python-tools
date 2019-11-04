import json
import os
from urllib.request import urlretrieve

import utils


# Another thing, parse version data, and if its already a buildid, then use that, otherwise, convert.

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


def grabKeys(device, version):
    buildid = utils.iOSToBuildid(device, version)
    url = f'https://api.ipsw.me/v4/keys/ipsw/{device}/{buildid}'
    utils.downloadJSONData(url, 'keys')
    with open('keys.json', 'r') as file:
        data = json.load(file)
        i = 0
        buildidFromJsonFile = data['buildid']
        while buildidFromJsonFile != buildid:
            i += 1
            buildidFromJsonFile = data['buildid']

        for stuff in data['keys']:
            print('Image: ' + stuff['image'])
            print('Filename: ' + stuff['filename'])
            print('KBAG: ' + stuff['kbag'])
            print('IV: ' + stuff['iv'])
            print('Key: ' + stuff['key'] + '\n')

        file.close()
        os.remove('keys.json')


def getBasebandVersion(device, version):
    buildid = utils.iOSToBuildid(device, version)
    url = f'https://api.ipsw.me/v4/keys/ipsw/{device}/{buildid}'
    utils.downloadJSONData(url, 'keys')
    with open('keys.json', 'r') as file:
        data = json.load(file)
        baseband = data['baseband']
        file.close()
        return baseband


def signed(device, version):
    buildid = utils.iOSToBuildid(device, version)
    linksForDevice(device)
    with open(f'{device}.json', 'r') as file:
        data = json.load(file)
        i = 0
        buildidFromJsonFile = data['firmwares'][i]['buildid']
        while buildidFromJsonFile != buildid:
            i += 1
            buildidFromJsonFile = data['firmwares'][i]['buildid']

        ios = data['firmwares'][i]['version']

        if data['firmwares'][i]['signed']:
            print(f'iOS {ios} ({buildid}) IS signed!')

        else:
            print(f'iOS {ios} ({buildid}) IS NOT signed!')