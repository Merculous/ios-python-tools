import os
import json
from urllib.request import urlopen

try:
    from .ipswapi import APIParser
    from .manifest import BuildManifest
    from .template import Template
except:
    raise ImportError


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
            api = APIParser(self.device, self.version)
            buildid = api.iOSToBuildid()
        except:
            raise ConnectionError

        template = Template()

        path = 'BuildManifest.plist'

        if os.path.exists(path):  # Also, just in case if the user terminated
            # So we don't have a leftover manifest that isn't the same device and or iOS
            os.remove(path)

        try:
            api.downloadManifest()  # To keep data "constant" we need to download every time
        except:
            raise ConnectionError

        build_manifest = BuildManifest()
        # Get BuildManiest.plist codename, filenames, and file paths.
        manifest_data = build_manifest.extractData()
        codename = manifest_data['codename']

        wikiUrl = 'https://www.theiphonewiki.com/w/index.php?title={}_{}_({})&action=edit'.format(
            codename, buildid, self.device)
        try:
            request = urlopen(wikiUrl).read().decode('utf-8')
        except:
            raise ConnectionError
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
