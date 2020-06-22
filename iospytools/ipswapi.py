
import json
import os
import plistlib
import sys
from urllib.request import urlopen, urlretrieve

try:
    from remotezip import RemoteZip
except ImportError:
    raise

try:
    from .utils import showProgress
except ImportError:
    raise


class API(object):
    def __init__(self, device, version=None, buildid=None):
        super().__init__()

        self.device = device
        self.version = version
        self.buildid = buildid

    def getDeviceJSONData(self, filetype='ipsw'):
        # Returns JSON Data, rather than downloading each time, see below later on :P
        if filetype == 'ipsw':
            api_url = 'https://api.ipsw.me/v4/device/{}?type={}'.format(
                self.device, 'ipsw')
        elif filetype == 'ota':
            api_url = 'https://api.ipsw.me/v4/device/{}?type={}'.format(
                self.device, 'ota')
        else:
            raise ValueError('Only filetypes, "ipsw" and "ota" are supported!')

        try:
            r = urlopen(api_url).read().decode('utf-8')
        except ConnectionError:
            print('Failed to download JSON data!')
            raise
        else:
            return json.loads(r)

    def iOSToBuildid(self):
        # Easy to use function since we don't have to be paranoid about reading leftover json data :D
        data = self.getDeviceJSONData()
        for i in range(0, len(data['firmwares'])):
            if data['firmwares'][i]['version'] == self.version:
                return data['firmwares'][i]['buildid']

    def getArchiveURL(self, filetype='ipsw'):
        if filetype == 'ipsw':
            api_url = 'https://api.ipsw.me/v4/ipsw/{}/{}'.format(
                self.device, self.iOSToBuildid())
        elif filetype == 'ota':
            # TODO Add ota support
            pass
        else:
            raise ValueError('Only filetypes, "ipsw" and "ota" are supported!')

        r = urlopen(api_url).read().decode('utf-8')
        data = json.loads(r)
        url = data['url']
        return url

    def downloadIPSW(self):
        # TODO Use given hashes to determine if we need to download a genuine copy or not
        url = self.getArchiveURL()
        ipsw_name = os.path.basename(url)
        if not os.path.exists(ipsw_name):
            print('URL: {}'.format(url))
            print('File: {}'.format(ipsw_name))
            urlretrieve(url, ipsw_name, showProgress)
        else:
            sys.exit('{} already exists!'.format(ipsw_name))

    # TODO Add beta support CC @mcg29

    def getSignedVersions(self, beta=False):
        data = self.getDeviceJSONData()
        signed = list()
        for i in range(0, len(data['firmwares'])):
            version_from_json = data['firmwares'][i]['version']
            buildid_from_json = data['firmwares'][i]['buildid']
            signature_from_json = data['firmwares'][i]['signed']
            if signature_from_json:
                stuff = {
                    'iOS': version_from_json,
                    'buildid': buildid_from_json,
                    'signed': signature_from_json,
                    'filetype': 'ipsw'
                }
                if stuff not in signed:
                    signed.append(stuff)

        data = self.getDeviceJSONData('ota')
        for i in range(0, len(data['firmwares'])):
            version_from_json = data['firmwares'][i]['version']
            buildid_from_json = data['firmwares'][i]['buildid']
            signature_from_json = data['firmwares'][i]['signed']
            if signature_from_json:
                stuff = {
                    'iOS': version_from_json,
                    'buildid': buildid_from_json,
                    'signed': signature_from_json,
                    'filetype': 'ota'
                }
                if stuff not in signed:
                    signed.append(stuff)

        return signed

    def downloadFileFromArchive(self, path, filetype='ipsw'):
        url = self.getArchiveURL()
        if filetype == 'ipsw':
            with RemoteZip(url) as f:
                files = f.namelist()
                if not os.path.exists(path):
                    if path in files:
                        print('Downloading: {}'.format(path))
                        f.extract(path)
                else:
                    raise FileExistsError('{} already exists!'.format(path))

        elif filetype == 'ota':
            # TODO Add ota support
            pass

        else:
            raise ValueError('Only filetypes, "ipsw" and "ota" are supported!')

    # Same as above but we don't download, which does help with leftover json data and such

    def readFileFromArchive(self, path):
        url = self.getArchiveURL()
        with RemoteZip(url) as f:
            data = f.read(path)
            return data

    def getCodename(self):
        data = self.readFileFromArchive('BuildManifest.plist')
        stuff = plistlib.loads(data)
        codename = stuff['BuildIdentities'][0]['Info']['BuildTrain']
        return codename
