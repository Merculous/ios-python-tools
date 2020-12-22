
import json
import os
import sys
from urllib.request import urlopen, urlretrieve

try:
    from remotezip import RemoteZip
except ImportError:
    raise

try:
    from utils import showProgress
except ImportError:
    raise


class API(object):
    def __init__(self, device=None, version=None, buildid=None, ota=False, beta=False) -> None:
        super().__init__()

        self.device = device
        self.version = version
        self.buildid = buildid
        self.ota = ota
        self.beta = beta

    def getDeviceJSONData(self) -> dict:
        '''

        Returns a dict which contains keys: beta, type, data

        beta is by default False

        type is by default ipsw

        data is the device's json data returned from api.ipsw.me

        '''

        if self.device:
            filetype = 'ipsw'
            is_beta = False

            if self.ota:  # Beta info is inside ota data
                filetype = 'ota'

            if self.beta:
                filetype = 'ota'
                is_beta = True

            api_url = 'https://api.ipsw.me/v4/device/{}?type={}'.format(
                self.device, filetype)

            r = urlopen(api_url).read().decode('utf-8')
            data = json.loads(r)
            info = {
                'beta': is_beta,
                'type': filetype,
                'data': data  # This our actual data from ipsw.me
            }
            return info
        else:
            sys.exit('[getDeviceJSONData] No device was passed!')

    def iOSToBuildid(self) -> list:
        '''
        Returns a list of dicts containing: version, buildid, type, beta

        version is the passed in value from user

        buildid is the or a conversion from the iOS to its build number

        type and beta are passed down from getDeviceJSONData

        '''

        if self.version:
            data = self.getDeviceJSONData()
            firmwares = data['data']['firmwares']
            buildids = list()
            for i in range(0, len(firmwares)):
                version = firmwares[i]['version']
                buildid = firmwares[i]['buildid']
                if version == self.version:
                    info = {
                        'version': version,
                        'buildid': buildid,
                        'type': None,
                        'beta': False
                    }
                    # Only passed beta
                    if data['beta']:
                        if 'releasetype' in firmwares[i]:
                            releasetype = firmwares[i]['releasetype']
                            if releasetype == 'Beta':
                                info['type'] = 'ota'
                                info['beta'] = True
                                if info not in buildids:
                                    buildids.append(info)

                    # Only passed ota
                    elif data['type'] == 'ota' and not data['beta']:
                        if 'releasetype' in firmwares[i]:
                            releasetype = firmwares[i]['releasetype']
                            if releasetype == '':
                                info['type'] = 'ota'
                                if info not in buildids:
                                    buildids.append(info)

                    # Only passed ipsw
                    else:
                        info['type'] = 'ipsw'
                        if info not in buildids:
                            buildids.append(info)

            if buildids:
                return buildids
            else:
                sys.exit('[iOSToBuildid] No buildid\'s were found!')

        else:
            sys.exit('[iOSToBuildid] No version was passed!')

    # TODO Allow selecting more than one buildid

    def getArchiveURL(self):
        data = self.getDeviceJSONData()
        firmwares = data['data']['firmwares']
        urls = list()

        if self.version and not self.buildid:  # Only passed version
            buildids = self.iOSToBuildid()

            if len(buildids) > 1:
                for i in range(0, len(buildids)):
                    print('{}: {}'.format(i, buildids[i]['buildid']))
                choice = input(
                    'Got more than one value! Press the equivalent number key and enter.\n')
                for ii in range(0, len(firmwares)):
                    buildid = firmwares[ii]['buildid']
                    if buildids[int(choice)]['buildid'] == buildid:
                        url = firmwares[ii]['url']
                        if url not in urls:
                            urls.append(url)

            else:
                for i in range(0, len(firmwares)):
                    buildid = firmwares[i]['buildid']
                    if buildids[0]['buildid'] == buildid:
                        url = firmwares[i]['url']
                        if url not in urls:
                            # If ota, can have multiple archives
                            urls.append(url)

        elif self.buildid and not self.version:  # Only passed buildid
            for i in range(0, len(firmwares)):
                buildid = firmwares[i]['buildid']
                if buildid == self.buildid:
                    url = firmwares[i]['url']
                    urls.append(url)

        else:
            sys.exit('[getArchiveURL] No version or buildid passed!')

        if urls:
            return ''.join(urls)
        else:
            sys.exit('[getArchiveURL] No url found!')

    def downloadArchive(self, path=None):
        url = self.getArchiveURL()
        name = os.path.basename(url)
        print('Downloading: {}'.format(name))
        urlretrieve(url, name, showProgress)

    def downloadFileFromArchive(self, file: str, out=False):
        url = self.getArchiveURL()
        data = RemoteZip(url).read(file)
        with open(file, 'wb') as f:
            f.write(data)
            f.close()
