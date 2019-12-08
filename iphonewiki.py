import json
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup

import ipswapi
import utils

"""

Syntax for uploading keys (will be added soon):

If the device is not an iPhone or a cellular iPad, delete the Baseband parameter.

If the device is an Apple TV (iOS versions), set Version to the marketing version with the internal version in parenthesis.

For each *, *IV, and *Key section, put the file name on the first line. If the item is the Root FS or a ramdisk,
remove the .dmg file extension. If that firmware item does not exist in that firmware, delete its parameter section.
If the firmware item is not encrypted, set *IV to "Not Encrypted" and delete the *Key parameter. If the key/iv is not known,
then the KBAG should be added.

For devices such as iPhone 6s that have two sets of files such as N71AP and N71mAP, then a second file can be added underneath
with a "2" at the end of the name. For example, you can have AppleLogo and AppleLogo2 blocks.

For DownloadURL, do not place anything other than URLs to free firmwares hosted on Apple Inc.'s servers. For beta firmwares, delete the parameter.

"""


def parseWiki(device, version):
    buildid = utils.iOSToBuildid(device, version)
    codename = getCodename(device, version)
    wikiUrl = f'https://www.theiphonewiki.com/w/index.php?title={codename}_{buildid}_({device})&action=edit'
    request = urlopen(wikiUrl).read().decode('utf-8')
    return request.split('{{keys')[1].split('}}')[0].replace('|', '')


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
        yeet = soup.find_all('a', text=f'{version}')
        for codename in yeet:
            lolList = codename['title'].split()
            deviceWiki = f'({device})'
            if lolList[1] == buildid and lolList[2] == deviceWiki:
                file.close()
                os.remove(f'{device}.json')
                return lolList[0]
            else:
                continue


def getBasebandVersion(device, version):
    data = parseWiki(device, version).splitlines()
    return data[5].replace('Baseband            =', '').strip()

