
import asyncio

from .remote import getURLData

class WIKI:
    base_url = 'https://www.theiphonewiki.com'

    def __init__(self, session, codename, buildid, identifier):
        self.session = session
        self.codename = codename
        self.buildid = buildid
        self.identifier = identifier


    async def readFirmwareKeysPage(self):
        url = self.base_url + f'/w/index.php?title={self.codename}_{self.buildid}_({self.identifier})&action=raw'
        data = await getURLData(self.session, url)
        return data


    async def parseTemplate(self):
        data = await self.readFirmwareKeysPage()
        data = data.splitlines()

        info = {}

        for line in data:
            if line.startswith(' | '):
                line = line.replace(' | ', '').split('=')
                key = line[0].strip()
                value = line[1].strip()

                info[key] = value

        return info
