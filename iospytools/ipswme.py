
import json

from enquiries import choose

from .remote import getURLData


class IPSWAPI:
    base_url = 'https://api.ipsw.me/v4'

    def __init__(self, session, device=None, version=None, ota=None, beta=None) -> None:
        self.session = session
        self.device = device
        self.version = version
        self.ota = ota
        self.beta = beta

    async def getAllDevices(self) -> dict:
        url = f'{self.base_url}/devices'
        data = await getURLData(self.session, url)
        return json.loads(data)

    async def getDeviceInfo(self) -> dict:
        if self.device:
            devices = await self.getAllDevices()
            for device in devices:
                ident = device['identifier']
                if self.device == ident:
                    url = f'{self.base_url}/device/{self.device}'
                    if self.ota:
                        url = f'{url}?type=ota'
                    else:
                        url = f'{url}?type=ipsw'
                    data = await getURLData(self.session, url)
                    return json.loads(data)
        else:
            raise ValueError('No device was passed!')

    async def iOSToBuildid(self) -> str:
        if self.device and self.version:
            info = await self.getDeviceInfo()
            firmwares = info['firmwares']
            matches = []
            for firmware in firmwares:
                iOS = firmware['version']
                buildid = firmware['buildid']
                if self.version == iOS:
                    if buildid not in matches:
                        matches.append(buildid)
            return matches
        else:
            raise ValueError('No device or iOS version was passed!')

    async def getArchiveURL(self) -> str:
        if self.device and self.version:
            info = await self.getDeviceInfo()
            firmwares = info['firmwares']
            buildids = await self.iOSToBuildid()
            if len(buildids) == 1:
                for firmware in firmwares:
                    if firmware['buildid'] == buildids[0]:
                        return firmware['url']
            else:
                prompt = 'Please select which version you\'d like to use.'
                choice = choose(prompt, buildids)
                for firmware in firmwares:
                    if firmware['buildid'] == choice:
                        return firmware['url']

    async def getSignedVersions(self) -> list:
        if self.device:
            info = await self.getDeviceInfo()
            firmwares = info['firmwares']
            signed = []
            for firmware in firmwares:
                if firmware['signed']:
                    tmp = (firmware['version'], firmware['buildid'])
                    if tmp not in signed:
                        signed.append(tmp)
        else:
            raise ValueError('No device was passed!')
