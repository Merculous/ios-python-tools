import json
import os
from urllib.request import urlretrieve

from utils import downloadJSONData, progress, splitToFileName


"""

This is mainly the heart of the script.

Handles data from ipsw.me api

"""

class APIParser:
    def __init__(self, device, version):
        super().__init__()
        self.device = device
        self.version = version


    def linksForDevice(self, device): # TODO Add OTA compatibility
        url = f'https://api.ipsw.me/v4/device/{device}?type=ipsw'
        return downloadJSONData(url, device)


    def iOSToBuildid(self, device, version):
        self.linksForDevice(self.device)
        with open(f'{self.device}.json', 'r') as file:
            data = json.load(file)
            i = 0
            iOSFromJsonFile = data['firmwares'][i]['version']
            while iOSFromJsonFile != version:
                i += 1
                iOSFromJsonFile = data['firmwares'][i]['version']

            buildid = data['firmwares'][i]['buildid']

        file.close()
        return buildid


    def downloadIPSW(self, device, version): # TODO Add OTA compatibility
        buildid = self.iOSToBuildid(self.device, self.version)
        self.linksForDevice(self.device)
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


    def signed(self, device): # TODO Add OTA compatibility
        signedVersions = []
        self.linksForDevice(self.device)
        with open(f'{self.device}.json', 'r') as file:
            data = json.load(file)
            for stuff in data['firmwares']:
                ios = stuff['version']
                buildid = stuff['buildid']
                signed = stuff['signed']
                if signed:
                    version = [ios, buildid]
                    signedVersions.append(version)

        file.close()
        return signedVersions
