
import json
from urllib.request import urlopen, urlretrieve

import enquiries
from remotezip import RemoteZip


class API(object):
    def __init__(self, device=None, version=None, buildid=None, beta=None) -> None:
        super().__init__()

        self.device = device
        self.version = version
        self.buildid = buildid
        self.beta = beta

        self.base_url = 'https://api.ipsw.me/v4'

    def getAllDevices(self) -> list:
        url = f'{self.base_url}/devices'
        r = urlopen(url).read()
        data = json.loads(r)
        return data

    def getDeviceData(self, restore_type: str) -> dict:
        if self.device:
            supported = ('ipsw', 'ota')
            if restore_type in supported:
                devices = self.getAllDevices()
                for device in devices:
                    if device['identifier'] == self.device:
                        url = f'{self.base_url}/device/{self.device}?type={restore_type}'
                        r = urlopen(url).read()
                        data = json.loads(r)
                        return data

            else:
                raise ValueError(f'Unknown restore type: {restore_type}')
        else:
            raise ValueError('No device was passed!')

    def iOSToBuildid(self) -> dict:
        if self.version:
            info = dict()
            restore_type = 'ipsw'
            device_ipsw = self.getDeviceData(restore_type)
            ipsw_firmwares = device_ipsw['firmwares']

            for i in range(len(ipsw_firmwares)):
                version = ipsw_firmwares[i]['version']
                buildid = ipsw_firmwares[i]['buildid']

                if version.endswith(self.version):
                    if version not in info:
                        info[version] = list()

                    tmp = {
                        'type': restore_type,
                        'buildid': buildid,
                        'beta': False
                    }

                    if tmp not in info[version]:
                        info[version].append(tmp)

                else:
                    continue

            # OTA wasn't added until iOS 5. We need to check
            # and only run the code below if our version is >=5.x.x

            skips = ('1.', '2.', '3.', '4.')

            for skip in skips:
                if self.version.startswith(skip):
                    return info

            i = 0
            restore_type = 'ota'

            device_ota = self.getDeviceData(restore_type)
            ota_firmwares = device_ota['firmwares']

            for i in range(len(ota_firmwares)):
                version = ota_firmwares[i]['version']
                buildid = ota_firmwares[i]['buildid']
                releasetype = ota_firmwares[i]['releasetype']

                if version.endswith(self.version):
                    if version not in info:
                        info[version] = list()

                    tmp = {
                        'type': restore_type,
                        'buildid': buildid,
                        'beta': bool
                    }

                    if releasetype == 'Beta':
                        tmp['beta'] = True
                    else:
                        tmp['beta'] = False

                    if tmp not in info[version]:
                        info[version].append(tmp)
                else:
                    continue

            return info

        else:
            raise ValueError('No version was passed!')
