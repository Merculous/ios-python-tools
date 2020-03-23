import os
import re

import xmltodict

from ipswapi import APIParser


class Manifest(object):  # TODO Add OTA compatibility
    def __init__(self, path='BuildManifest.plist'):
        super().__init__()

        self.path = path

    def extractData(self):
        with open(self.path, 'r') as f:  # path will default to BuildManifest.plist, unless user provides custom
            data = xmltodict.parse(f.read())
            buildid = data['plist']['dict']['string'][0]
            iOS = data['plist']['dict']['string'][1]
            device = data['plist']['dict']['array'][1]['string']
            codename = data['plist']['dict']['array'][0]['dict'][0]['dict'][0]['string'][1]
            files = data['plist']['dict']['array'][0]['dict'][0]['dict'][1]['dict']
            file_paths = list()

            for stuff in files:  # To help with crammed view in debugger
                file_paths.append(stuff['dict']['string'])  # File paths

        # TODO Fix parsing manifests with multiple devices. iPhone6,1 10.3.3 'files' gives output of n69 instead of its n51

        f.close()

        info = {
            'device': device,
            'ios': iOS,
            'buildid': buildid,
            'codename': codename,
            'files': file_paths
        }
        return info

    def getCodename(self):
        return self.extractData()['codename']  # Always works :D

    def getFilePaths(self):
        return self.extractData()['files']

    def getBasebandVersion(self):
        pass
