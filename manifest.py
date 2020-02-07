import json
import os

from remotezip import RemoteZip

from ipswapi import APIParser


class Manifest: # # TODO Add OTA compatibility
    def __init__(self, device, version):
        super().__init__()
        self.device = device
        self.version = version


    def downloadBuildManifest(self, device, version):
        shit = APIParser(self.device, self.version)
        buildid = shit.iOSToBuildid(self.device, self.version)
        shit.linksForDevice(self.device)

        with open(f'{self.device}.json', 'r') as file:
            data = json.load(file)
            i = 0
            buildidFromJsonFile = data['firmwares'][i]['buildid']
            while buildidFromJsonFile != buildid:
                i += 1
                buildidFromJsonFile = data['firmwares'][i]['buildid']

            url = data['firmwares'][i]['url']
            manifest = 'BuildManifest.plist'

            # Start the process of reading and extracting a file from a url

            print(f'Downloading manifest for {self.version}, {buildid}')
            zip = RemoteZip(url)
            zip.extract(manifest)
            # This can be done better
            os.rename(manifest, f'BuildManifest_{self.device}_{self.version}_{buildid}.plist')
            print('Done downloading!')
            zip.close()

        file.close()


    def getCodename(self, manifest):
        pass


    def getBasebandVersion(self, manifest):
        pass


    def iOSToBuildid(self, manifest):
        pass
