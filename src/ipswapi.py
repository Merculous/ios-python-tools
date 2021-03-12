
import json
import os
from urllib.request import urlopen, urlretrieve

import enquiries
from remotezip import RemoteZip

# from .iphonewiki import Wiki
from .manifest import Manifest
from .utils import showProgress


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
        supported = ('iPhone', 'iPad', 'iPod', 'AppleTV')
        devices = list()

        for device in data:
            for devicetype in supported:
                if device['identifier'].startswith(devicetype):
                    if device not in devices:
                        devices.append(device)

        return devices

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

            # We can have more than one "version" and or buildid
            # Init user interaction

            tmp1 = list()

            for value1 in info:
                if value1 not in tmp1:
                    tmp1.append(value1)

            if len(tmp1) > 1:
                prompt1 = 'Please select which version you\'d like to use.'
                choice1 = enquiries.choose(prompt1, tmp1)
            else:
                choice1 = tmp1[0]

            buildids = list()

            for value2 in info[choice1]:
                if value2 not in buildids:
                    buildids.append(value2)

            if len(buildids) > 1:
                prompt2 = 'Please select which buildid you\'d like to use.'
                choice2 = enquiries.choose(prompt2, buildids)
                return choice2
            else:
                return buildids[0]

        else:
            raise ValueError('No version was passed!')

    def getArchiveURL(self) -> str:
        # I want to be absolutely sure we have the correct info.
        # Because of this, I will just use my self.iOSToBuildid()
        # function. This means, I'm going to ignore self.buildid
        # and self.beta. My function will give you all three.
        info = self.iOSToBuildid()
        data = self.getDeviceData(info['type'])
        firmwares = data['firmwares']

        for i in range(len(firmwares)):
            version = firmwares[i]['version']
            buildid = firmwares[i]['buildid']

            if version == self.version and buildid == info['buildid']:
                url = firmwares[i]['url']
                return url

    def downloadArchive(self, path=None) -> None:
        url = self.getArchiveURL()
        name = os.path.basename(url)

        if not path:
            path = name

        if not os.path.isfile(path):
            print(f'Downloading: {path}')
            # Defaults to saving in current directory
            urlretrieve(url, path, showProgress)
        else:
            raise FileExistsError(f'{path} already exists!')

    # TODO fix finding BuildManifest.plist

    def readFromRemoteArchive(self, path: str, save: bool, out=None) -> bytes:
        url = self.getArchiveURL()

        with RemoteZip(url) as f:
            data = f.read(path)

            if save:
                name = os.path.basename(path)

                if out:
                    if os.path.isdir(out):
                        name = f'{out}/{name}'

                if not os.path.exists(name):
                    with open(name, 'wb') as ff:
                        ff.write(data)

                else:
                    raise FileExistsError(f'{name} already exists!')
            else:
                return data

    def getSignedVersions(self) -> dict:
        tmp1 = list()

        if not self.device:
            devices = self.getAllDevices()

            for device in devices:
                if device['identifier'] not in tmp1:
                    tmp1.append(device['identifier'])
        else:
            tmp1.append(self.device)

        info = dict()

        # TODO Clean up code when using only one device. Make loops more efficient.

        for value in tmp1:

            if len(tmp1) > 1:
                self.device = value

            data_ipsw = self.getDeviceData('ipsw')
            firmware_ipsw = data_ipsw['firmwares']

            for i in range(len(firmware_ipsw)):
                version = firmware_ipsw[i]['version']
                buildid = firmware_ipsw[i]['buildid']
                is_signed = firmware_ipsw[i]['signed']

                if is_signed:
                    if version not in info:
                        info[version] = dict()
                        info[version]['ipsw'] = dict()
                        info[version]['ipsw']['buildid'] = list()

                        if buildid not in info[version]['ipsw']['buildid']:
                            info[version]['ipsw']['buildid'].append(buildid)

                        if len(tmp1) > 1:
                            info[version]['ipsw']['device'] = list()
                            if self.device not in info[version]['ipsw']['device']:
                                info[version]['ipsw']['device'].append(
                                    self.device)
                else:
                    continue

            data_ota = self.getDeviceData('ota')
            firmware_ota = data_ota['firmwares']

            for ii in range(len(firmware_ota)):
                version = firmware_ota[ii]['version']
                buildid = firmware_ota[ii]['buildid']
                is_signed = firmware_ota[ii]['signed']

                if is_signed:
                    if version not in info:
                        info[version] = dict()
                        info[version]['ota'] = dict()
                        info[version]['ota']['buildid'] = list()

                        if buildid not in info[version]['ota']['buildid']:
                            info[version]['ota']['buildid'].append(buildid)

                        if len(tmp1) > 1:
                            info[version]['ota']['device'] = list()
                            if self.device not in info[version]['ota']['device']:
                                info[version]['ota']['device'].append(
                                    self.device)

                else:
                    continue

        return info

    def getCodename(self) -> str:
        data = self.readFromRemoteArchive('BuildManifest.plist', False)
        m = Manifest(data)
        codename = m.getInfo()['codename']
        return codename

    def getKeys(self) -> list:
        pass
