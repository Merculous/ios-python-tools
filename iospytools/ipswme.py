
import json

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
                    data = await getURLData(self.session, url)
                    return json.loads(data)
        else:
            raise ValueError('No device was passed!')

    async def iOSToBuildid(self) -> str:
        if self.device and self.version:
            info = await self.getDeviceInfo()
            firmwares = info['firmwares']
            for firmware in firmwares:
                iOS = firmware['version']
                buildid = firmware['buildid']
                if self.version == iOS:
                    return buildid
        else:
            raise ValueError('No iOS version wass passed!')
