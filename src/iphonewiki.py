from urllib.request import urlopen

from template import Template

class Wiki(object):
    def __init__(self, device, buildid, codename):
        super().__init__()

        self.device = device
        self.buildid = buildid
        self.codename = codename

    def getKeys(self):
        url = 'https://www.theiphonewiki.com/w/index.php?title={}_{}_({})&action=edit'.format(
            self.codename, self.buildid, self.device)
        r = urlopen(url).read().decode()
        t = Template(r)
        return t.parse()
