import json
import os
from urllib.request import urlretrieve

from remotezip import RemoteZip

from .utils import downloadJSONData, progress, splitToFileName


"""

This is mainly the heart of the script.

Handles data from ipsw.me api

"""


class APIParser(object):
    def __init__(self, device, version, ota=False, beta=False):
        super().__init__()
        self.device = device
        self.version = version
        self.ota = ota
        self.beta = beta

    def linksForDevice(self, filetype):
        url = f'https://api.ipsw.me/v4/device/{self.device}?type={filetype}'
        return downloadJSONData(url, self.device)

    def iOSToBuildid(self):
        self.linksForDevice('ipsw')
        with open(f'{self.device}.json', 'r') as file:
            data = json.load(file)
            i = 0
            iOSFromJsonFile = data['firmwares'][i]['version']
            while iOSFromJsonFile != self.version:
                i += 1
                iOSFromJsonFile = data['firmwares'][i]['version']

            buildid = data['firmwares'][i]['buildid']

        file.close()
        return buildid

    def downloadIPSW(self):
        buildid = self.iOSToBuildid()
        self.linksForDevice('ipsw')
        with open(f'{self.device}.json', 'r') as file:
            data = json.load(file)
            i = 0
            buildidFromJsonFile = data['firmwares'][i]['buildid']
            while buildidFromJsonFile != buildid:
                i += 1
                buildidFromJsonFile = data['firmwares'][i]['buildid']

            url = data['firmwares'][i]['url']
            ios = data['firmwares'][i]['version']
            filename = splitToFileName(url)

            print('Device:', self.device)
            print('iOS:', ios)
            print('Buildid:', buildidFromJsonFile)
            print('Filename:', filename)
            urlretrieve(url, filename, progress)
            print('\n')
        file.close()

    def signed(self):
        signedVersions = list()

        # Get ipsw signed versions

        self.linksForDevice('ipsw')
        with open(f'{self.device}.json', 'r') as file:
            data = json.load(file)
            for stuff in data['firmwares']:
                ios = stuff['version']
                buildid = stuff['buildid']
                status = stuff['signed']
                versions = [ios, buildid, 'ipsw']
                if status:  # If signed
                    signedVersions.append(versions)
        file.close()

        # Get ota signed versions

        self.linksForDevice('ota')
        with open(f'{self.device}.json', 'r') as f:
            data = json.load(f)
            for stuff in data['firmwares']:
                ios = stuff['version']
                if ios[0:3] == "9.9":  # Beginning with iOS 10, now versions also include 9.9 at the beginning, example, 9.9.10.3.3. Skip these.
                    pass
                else:
                    buildid = stuff['buildid']
                    status = stuff['signed']
                    currentOTA = [ios, buildid, 'ota']
                    if status:
                        if currentOTA not in signedVersions:
                            signedVersions.append(currentOTA)

        f.close()

        # TODO Clean up iOS 10 will have 9.9.10.3.3 for example. We need to print versions with unique buildids once, and if ipsw is signed, only print ipsw signed.

        # TODO Printed signed versions for iPhone4,1 still gives 9.3.5 ipsw and ota

        return signedVersions

    def downloadFileFromArchive(self, path, output=False):
        buildid = self.iOSToBuildid()
        self.linksForDevice('ipsw')
        with open(f'{self.device}.json', 'r') as file:
            data = json.load(file)
            i = 0
            buildidFromJsonFile = data['firmwares'][i]['buildid']
            while buildidFromJsonFile != buildid:
                i += 1
                buildidFromJsonFile = data['firmwares'][i]['buildid']

            url = data['firmwares'][i]['url']
            zip = RemoteZip(url)
            zip.extract(path)
            if output:
                os.rename(path, output)
            zip.close()

        file.close()

    def printURLForArchive(self):
        buildid = self.iOSToBuildid()
        self.linksForDevice('ipsw')
        with open(f'{self.device}.json', 'r') as file:
            data = json.load(file)
            i = 0
            buildidFromJsonFile = data['firmwares'][i]['buildid']
            while buildidFromJsonFile != buildid:
                i += 1
                buildidFromJsonFile = data['firmwares'][i]['buildid']

            url = data['firmwares'][i]['url']

        file.close()
        return url
