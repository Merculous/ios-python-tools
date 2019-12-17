import json
import os
from urllib.request import urlopen

from bs4 import BeautifulSoup

import ipswapi
import utils

def grabKeys(device, version):
    buildid = utils.iOSToBuildid(device, version)
    ipswapi.linksForDevice(device)
    with open(f'{device}.json', 'r') as file:
        data = json.load(file)
        i = 0
        buildidFromJsonFile = data['firmwares'][i]['buildid']
        while buildidFromJsonFile != buildid:
            i += 1
            buildidFromJsonFile = data['firmwares'][i]['buildid']

    file.close()
    os.remove(f'{device}.json')
