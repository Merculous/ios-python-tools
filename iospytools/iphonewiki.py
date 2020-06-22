from urllib.request import urlopen

try:
    from .ipswapi import API
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
    def getWikiKeys(self):
        api = API(self.device, self.version)
        buildid = api.iOSToBuildid()
        codename = api.getCodename()
        wikiUrl = 'https://www.theiphonewiki.com/w/index.php?title={}_{}_({})&action=edit'.format(
            codename, buildid, self.device)
        try:
            request = urlopen(wikiUrl).read().decode('utf-8')
        except ConnectionError:
            print('Failed to request data from iPhoneWiki!')
            raise
        else:
            template = Template()
            return template.parseTemplate(request)

    # TODO Maybe have it open an html file, the page to upload keys, importing template into the page, just needing to press "upload"

    def uploadWikiKeys(self):
        pass

    def checkWikiKeys(self):
        pass
