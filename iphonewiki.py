import json
import os
from urllib.request import urlopen

from bs4 import BeautifulSoup

import ipswapi
import utils


"""
Handles data on the iphonewiki page.

Grabs keys and baseband version.
"""


def getWikiKeys(device, version):
    buildid = utils.iOSToBuildid(device, version)
    codename = getCodename(device, version)
    wikiUrl = f'https://www.theiphonewiki.com/w/index.php?title={codename}_{buildid}_({device})&action=edit'
    request = urlopen(wikiUrl).read().decode('utf-8')
    data = request.split('{{keys')[1].split('}}')[0].replace('|', '').splitlines()
    del data[0:8] # Remove the top info we don't need
    for keys in data:
        print(keys)
  

# TODO I can just parse build manifest to get this    
def getCodename(device, version):
    buildid = utils.iOSToBuildid(device, version)
    ipswapi.linksForDevice(device)
    with open(f'{device}.json', 'r') as file:
        data = json.load(file)
        i = 0
        buildidFromJsonFile = data['firmwares'][i]['buildid']
        while buildidFromJsonFile != buildid:
            i += 1
            buildidFromJsonFile = data['firmwares'][i]['buildid']

        strip = version.split('.')[0] + '.x'
        url = f'https://www.theiphonewiki.com/wiki/Firmware_Keys/{strip}'
        stuff = urlopen(url).read().decode('utf-8')
        soup = BeautifulSoup(stuff, features='html.parser')
        yeet = soup.find_all('a', text=version)
        for codename in yeet:
            lolList = codename['title'].split()
            deviceWiki = f'({device})'
            if lolList[1] == buildid and lolList[2] == deviceWiki:
                file.close()
                os.remove(f'{device}.json')
                return lolList[0]
            else:
                continue

# TODO I can just parse build manifest to get this    

def getBasebandVersion(device, version):
    pass

