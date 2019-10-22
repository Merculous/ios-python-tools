import json
import sys
import os
from urllib.request import urlopen, Request, urlretrieve

import utils

# python3 -m json.tool < {device}.json to make readable json data

# TODO Make this more logical. Just get some practice with JSON and just get everything from that.
# Actual: Maybe just parse info about an ipsw, if we can even pass in a version rather than buildid.
# Another thing, parse version data, and if its already a buildid, then use that, otherwise, convert.

# I could just use this https://api.ipsw.me/v4/ipsw/version since it uses the actual version.
# This should also make things much easier to find, since it narrows down the data being read, which will
# make this "super" fast.


def linksForDevice(device):
    url = f'https://api.ipsw.me/v4/device/{device}?type=ipsw'
    json_data = urlopen(url).read()
    data = json.loads(json_data)
    with open(f'{device}.json', 'w') as write_file:
        json.dump(data, write_file, indent=4)


def versionToBuildid(device, version):
    url = f'https://api.ipsw.me/v3/{device}/{version}/buildid'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    data = urlopen(req).read()  # Throws an exception if there are more than one buildid's for an iOS, need json.
    buildid = data.decode()  # Must be decoded
    return buildid


def downloadIPSW(device, buildid):
    buildid = versionToBuildid(device, buildid)  # First time using my own function in another function :D
    linksForDevice(device)  # Get the json file
    with open(f'{device}.json', 'r') as file:
        data = json.load(file)
        i = 0
        buildidFromJsonFile = data['firmwares'][i]['buildid']
        while buildidFromJsonFile != buildid: # While the buildid we parse over isn't the one we are looking for
            i += 1
            buildidFromJsonFile = data['firmwares'][i]['buildid']

        url = data['firmwares'][i]['url']
        ios = data['firmwares'][i]['version']
        filename = utils.splitIPSWUrlToName(url)

        print(f'Device: {device}')
        print(f'iOS: {ios}')
        print(f'Buildid: {buildidFromJsonFile}')
        print(f'Filename: {filename}')
        urlretrieve(url, filename)
        file.close()
        os.remove(f'{device}.json')

    if buildidFromJsonFile != buildid:
        file.close()
        os.remove(f'{device}.json')
        sys.exit(f'Got {buildidFromJsonFile}, instead of {buildid}')


def grabKeys(device, buildid):
    buildid = versionToBuildid(device, buildid)
    url = f'https://api.ipsw.me/v4/keys/ipsw/{device}/{buildid}'
    json_data = urlopen(url).read()
    data = json.loads(json_data)
    with open('keys.json', 'w') as write_file:
        json.dump(data, write_file)
