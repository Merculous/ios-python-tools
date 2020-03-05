import json
import os
import re

from remotezip import RemoteZip

from ipswapi import APIParser


class Manifest(object):  # TODO Add OTA compatibility
    def __init__(self, device, version):
        super().__init__()
        self.device = device
        self.version = version

    def manifestParser(self, path):
        if not os.path.exists(path):
            api = APIParser(self.device, self.version)
            buildid = api.iOSToBuildid()
            api.downloadFileFromArchive('BuildManifest.plist', f'BuildManifest_{self.device}_{self.version}_{buildid}.plist')

        with open(path, 'r') as f:
            data = f.read().replace('\t', '').splitlines()
        f.close()
        return data

    def getCodename(self):
        api = APIParser(self.device, self.version)
        buildid = api.iOSToBuildid()
        manifest = f'BuildManifest_{self.device}_{self.version}_{buildid}.plist'
        data = self.manifestParser(manifest)
        control = data.index('<key>BuildTrain</key>')
        index = control + 1
        codename = re.sub('<[^>]*>', '', data[index])  # Cheeky HTML tag removal :D
        os.remove(manifest)
        return codename

    def getBasebandVersion(self):
        api = APIParser(self.device, self.version)
        buildid = api.iOSToBuildid()
        manifest = f'BuildManifest_{self.device}_{self.version}_{buildid}.plist'
        data = self.manifestParser(manifest)
        control = data.index('<key>BasebandFirmware</key>')  # 33, wrong, need the second (not particularly bad)
        print(control)
