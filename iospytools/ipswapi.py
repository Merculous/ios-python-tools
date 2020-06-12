import json
import os
from urllib.request import urlretrieve

try:
    from remotezip import RemoteZip
    from .utils import downloadJSONData, showProgress, splitToFileName
except:
    raise ImportError

"""

This is mainly the heart of the script.

Handles data from ipsw.me api

"""


class APIParser(object):
    def __init__(self, device, version, ota=False, beta=False):
        super().__init__()
        self.device = device
        self.version = version
        self.buildid = self.iOSToBuildid()
        self.ota = ota
        self.beta = beta

    def linksForDevice(self, filetype):
        try:
            url = 'https://api.ipsw.me/v4/device/{}?type={}'.format(
                self.device, filetype)
            return downloadJSONData(url, self.device)
        except:
            raise ConnectionError

    def iOSToBuildid(self):
        try:
            self.linksForDevice('ipsw')
        except:
            raise ConnectionError
        else:
            try:
                with open('{}.json'.format(self.device), 'r') as file:
                    data = json.load(file)
                    for i in range(0, len(data['firmwares'])):
                        if data['firmwares'][i]['version'] == self.version:
                            return data['firmwares'][i]['buildid']
            except:
                raise FileNotFoundError

        return ''

    def downloadIPSW(self):
        try:
            self.linksForDevice('ipsw')
        except:
            raise ConnectionError
        else:
            try:
                with open('{}.json'.format(self.device), 'r') as file:
                    data = json.load(file)
                    i = 0
                    buildidFromJsonFile = data['firmwares'][i]['buildid']
                    while buildidFromJsonFile != self.buildid:
                        i += 1
                        buildidFromJsonFile = data['firmwares'][i]['buildid']

                    url = data['firmwares'][i]['url']
                    ios = data['firmwares'][i]['version']
                    filename = splitToFileName(url)

                    print('Device:', self.device)
                    print('iOS:', ios)
                    print('Buildid:', buildidFromJsonFile)
                    print('Filename:', filename)
                    try:
                        urlretrieve(url, filename, showProgress)
                    except:
                        raise ConnectionError
            except:
                raise FileNotFoundError

    def signed(self):
        # Get ipsw signed versions
        try:
            self.linksForDevice('ipsw')
        except:
            raise ConnectionError
        else:
            try:
                with open('{}.json'.format(self.device), 'r') as file:
                    signedVersions = list()
                    data = json.load(file)
                    for stuff in data['firmwares']:
                        ios = stuff['version']
                        buildid = stuff['buildid']
                        status = stuff['signed']
                        versions = [ios, buildid, 'ipsw']
                        if status:  # If signed
                            signedVersions.append(versions)
            except:
                raise FileNotFoundError

        # Get ota signed versions
        try:
            self.linksForDevice('ota')
        except:
            raise ConnectionError
        else:
            try:
                with open('{}.json'.format(self.device), 'r') as f:
                    data = json.load(f)
                    for stuff in data['firmwares']:
                        ios = stuff['version']
                        # Beginning with iOS 10, now versions also include 9.9 at the beginning, example, 9.9.10.3.3. Skip these.
                        if ios[0:3] == "9.9":
                            pass
                        else:
                            buildid = stuff['buildid']
                            status = stuff['signed']
                            currentOTA = [ios, buildid, 'ota']
                            if status:
                                if currentOTA not in signedVersions:
                                    signedVersions.append(currentOTA)
            except:
                raise FileNotFoundError

        # TODO Clean up iOS 10 will have 9.9.10.3.3 for example. We need to print versions with unique buildids once, and if ipsw is signed, only print ipsw signed.

        # TODO Printed signed versions for iPhone4,1 still gives 9.3.5 ipsw and ota

        return signedVersions

    def downloadFileFromArchive(self, path, output=False):
        try:
            self.linksForDevice('ipsw')
        except:
            raise ConnectionError
        else:
            try:
                with open('{}.json'.format(self.device), 'r') as file:
                    data = json.load(file)
                    i = 0
                    buildidFromJsonFile = data['firmwares'][i]['buildid']
                    while buildidFromJsonFile != self.buildid:
                        i += 1
                        buildidFromJsonFile = data['firmwares'][i]['buildid']

                    url = data['firmwares'][i]['url']
                    try:
                        with RemoteZip(url, timeout=5.0) as zip:
                            zip.extract(path)
                    except:
                        raise ConnectionError
                    finally:
                        if output:
                            os.rename(path, output)
            except:
                raise FileNotFoundError

    def printURLForArchive(self):
        try:
            self.linksForDevice('ipsw')
        except:
            raise ConnectionError
        else:
            try:
                with open('{}.json'.format(self.device), 'r') as file:
                    data = json.load(file)
                    i = 0
                    buildidFromJsonFile = data['firmwares'][i]['buildid']
                    while buildidFromJsonFile != self.buildid:
                        i += 1
                        buildidFromJsonFile = data['firmwares'][i]['buildid']

                    url = data['firmwares'][i]['url']

                return url
            except:
                raise FileNotFoundError

    def downloadManifest(self):
        try:
            return self.downloadFileFromArchive('BuildManifest.plist')
        except:
            raise ConnectionError
