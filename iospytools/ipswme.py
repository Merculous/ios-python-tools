
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
