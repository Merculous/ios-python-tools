import os
from urllib.request import urlopen

from ipswapi import APIParser
from manifest import Manifest


class iPhoneWiki(object):
    def __init__(self, device, version, ota=False, beta=False):
        super().__init__()
        self.device = device
        self.version = version
        self.ota = ota
        self.beta = beta

        """
        Handles data on the iphonewiki page.

        Grabs keys and codename.
        """

    def getWikiKeys(self):  # TODO Add OTA compatibility
        api = APIParser(self.device, self.version)
        buildid = api.iOSToBuildid()

        if not os.path.exists('BuildManifest.plist'):
            api.downloadFileFromArchive('BuildManifest.plist')

        lol = Manifest()
        codename = lol.getCodename()

        wikiUrl = f'https://www.theiphonewiki.com/w/index.php?title={codename}_{buildid}_({self.device})&action=edit'
        request = urlopen(wikiUrl).read().decode('utf-8')
        data = request.split('{{keys')[1].split('}}')[0].replace('|', '').splitlines()
        del data[0:8]  # Remove the top info we don't need
        return data

    def uploadWikiKeys(self):
        pass

    def checkWikiKeys(self):
        pass
