import json
import os
from urllib.request import urlopen

from bs4 import BeautifulSoup


"""
Handles data on the iphonewiki page.

Grabs keys and baseband version.
"""

class iPhoneWiki:
    def __init__(self, device, version):
        super().__init__()
        self.device = device
        self.version = version


    def getWikiKeys(self, device, version): # TODO Add OTA compatibility
        codename = None
        buildid = None
        wikiUrl = f'https://www.theiphonewiki.com/w/index.php?title={codename}_{buildid}_({device})&action=edit' # TODO
        request = urlopen(wikiUrl).read().decode('utf-8')
        data = request.split('{{keys')[1].split('}}')[0].replace('|', '').splitlines()
        del data[0:8] # Remove the top info we don't need
        for keys in data:
            print(keys)


    def uploadWikiKeys(self, device, version):
        pass


    def checkWikiKeys(self, device, version):
        pass
