from urllib.request import urlopen

from .template import Template


class Wiki:
    def __init__(self, device: str, buildid: str, codename: str):
        self.device = device
        self.buildid = buildid
        self.codename = codename

        self.api = 'https://www.theiphonewiki.com/w/api.php'

    # TODO Add OTA and Beta support, if I specifially need to specify it

    def requestKeys(self) -> list:
        url = 'https://www.theiphonewiki.com/w/index.php?title={}_{}_({})&action=edit'.format(
            self.codename, self.buildid, self.device)
        r = urlopen(url).read().decode()
        t = Template(r)
        return t.parse()
