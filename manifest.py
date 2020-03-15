import os
import re

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
        strings = []
        for stuff in data:
            if stuff.endswith('bbfw</string>'):
                if stuff not in strings:
                    strings.append(stuff)
        versions = re.findall(r"[0-9.]*[0-9]+", str(strings))  # regex check for numbers, and periods
        os.remove(manifest)
        return max(versions, key=len)  # TODO This can be done much much much better, plus some have more than one baseband so I need to fix this
