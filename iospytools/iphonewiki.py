import sys
from urllib.request import urlopen

try:
    from .ipswapi import API
    from .template import Template
except ImportError:
    raise


class iPhoneWiki(object):
    def __init__(self, device, version, buildid=False, codename=False, ota=False, beta=False):
        super().__init__()
        self.device = device
        self.version = version
        self.ota = ota
        self.beta = beta

        if buildid:
            self.buildid = buildid
        else:
            api = API(self.device, self.version)
            self.buildid = api.iOSToBuildid()

        if codename:
            self.codename = codename
        else:
            api = API(self.device, self.version)
            self.codename = api.getCodename()

        """
        Handles data on the iphonewiki page.

        Grabs key template from source code ;P
        """

    # TODO Make this check if the url is good. Probably have a dict saying like is got a response, or if there's
    # no keys for a particular device, iOS, etc.

    # Status codes:

    # 200, response was sent successfully

    # I need to check if there's even keys first

    def getWikiKeys(self):
        wikiUrl = 'https://www.theiphonewiki.com/w/index.php?title={}_{}_({})&action=edit'.format(
            self.codename, self.buildid, self.device)  # This is used for "ipsw" and "beta"
        response = urlopen(wikiUrl).read().decode('utf-8')
        if 'You can view and copy the source of this page.' not in response:
            sys.exit('Seems like there are no keys for: {} {} {}!'.format(
                self.device, self.version, self.buildid))
        else:
            template = Template()
            return template.parseTemplate(response)

    # TODO Maybe have it open an html file, the page to upload keys, importing template into the page, just needing to press "upload"

    def uploadWikiKeys(self):
        pass
