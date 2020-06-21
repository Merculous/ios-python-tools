import os
import json
from urllib.request import urlopen

try:
    from .ipswapi import API
    from .manifest import BuildManifest
    from .template import Template
except ImportError:
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

    # TODO Add OTA compatibility, allow single file grabbing
    def getWikiKeys(self, save=False, file=False):
        try:
            api = API(self.device, self.version)
            buildid = api.iOSToBuildid()
        except ConnectionError:
            print('Got an Apple or ipsw.me connection error!')
            raise

        template = Template()

        path = 'BuildManifest.plist'

        if os.path.exists(path):  # Also, just in case if the user terminated
            # So we don't have a leftover manifest that isn't the same device and or iOS
            os.remove(path)

        try:
            api.downloadManifest()  # To keep data "constant" we need to download every time
        except ConnectionError:
            print('Failed to download build manifest!')
            raise

        build_manifest = BuildManifest()
        # Get BuildManiest.plist codename, filenames, and file paths.
        manifest_data = build_manifest.extractData()
        codename = manifest_data['codename']

        wikiUrl = 'https://www.theiphonewiki.com/w/index.php?title={}_{}_({})&action=edit'.format(
            codename, buildid, self.device)
        try:
            request = urlopen(wikiUrl).read().decode('utf-8')
        except ConnectionError:
            print('Failed to request data from iPhoneWiki!')
            raise
        else:
            data = template.parseTemplate(request)
            if save:  # FIXME
                json_path = '{}_{}_{}.json'.format(
                    self.device, self.version, buildid)
                if path in os.listdir(os.getcwd()):
                    os.remove(path)
                with open(json_path, 'w') as f:
                    print('Writing contents to file...')
                    f.write(json.dumps(data))
                f.close()
            else:
                return data

    # TODO Maybe have it open an html file, the page to upload keys, importing template into the page, just needing to press "upload"

    def uploadWikiKeys(self):
        pass

    def checkWikiKeys(self):
        pass
