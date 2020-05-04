import os
from urllib.request import urlopen

try:
    from .ipswapi import APIParser
    from .manifest import BuildManifest
except ImportError as error:
    print('Oof, got error:', error)
    raise


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

    def getWikiKeys(self):  # TODO Add OTA compatibility, allow single file grabbing
        api = APIParser(self.device, self.version)
        buildid = api.iOSToBuildid()

        path = 'BuildManifest.plist'

        if os.path.exists(path):  # Also, just in case if the user terminated
            os.remove(path)  # So we don't have a leftover manifest that isn't the same device and or iOS

        api.downloadManifest()  # To keep data "constant" we need to download every time

        build_manifest = BuildManifest()
        codename = build_manifest.getCodename()

        wikiUrl = 'https://www.theiphonewiki.com/w/index.php?title={}_{}_({})&action=edit'.format(codename, buildid, self.device)
        request = urlopen(wikiUrl).read().decode('utf-8')
        data = request.split('{{keys')[1].split('}}')[0].replace('|', '').splitlines()
        del data[0:8]  # Remove the top info we don't need
        os.remove(path)
        return data

    # TODO Maybe have it open an html file, the page to upload keys, importing template into the page, just needing to press "upload"

    def uploadWikiKeys(self):
        pass

    def checkWikiKeys(self):
        pass
