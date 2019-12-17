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


def getKeys(device, version):
    data = parseWiki(device, version).strip()

    # Split off the extra info at the top

    """

    Version             = 3.0
    Build               = 7A341
    Device              = iPhone2,1
    Codename            = Kirkwood
    Baseband            = 04.26.08
    DownloadURL         = https://secure-appldnld.apple.com.edgesuite.net/content.info.apple.com/iPhone/061-6582.20090617.LlI87/iPhone2,1_3.0_7A341_Restore.ipsw 

    """


    # Add .dmg to the end of the dmg filenames


def getBasebandVersion(device, version):
    data = parseWiki(device, version).splitlines()
    return data[5].replace('Baseband            =', '').strip()
