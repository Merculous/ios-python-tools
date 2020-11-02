import os
import plistlib


class Bundle(object):
    def __init__(self, bundle=None):
        super().__init__()

        if not os.path.exists('FirmwareBundles'):
            os.mkdir('FirmwareBundles')

        try:
            os.path.isdir(bundle)
        except IOError:
            print('{} must be a directory!'.format(bundle))
            raise
        else:
            self.bundle = bundle

        try:
            os.path.exists('{}/Info.plist'.format(self.bundle))
        except FileNotFoundError:
            print('Info.plist does not exist in {}!'.format(self.bundle))
            raise

    def getInfo(self):
        # Making my own so we don't have to rely on plist tags
        # and whatnot. Don't want to deal with it.
        info = {
            'IPSWName': str,
            'IPSWHash': str,
            'RemoveManifest': bool,
            'Jailbroken': bool,
            'RootFS': {
                'RootFSFilename': str,
                'RootFSSize': int,
                'RootFSKey': str,
                'RootFSMountName': str,
                'Patches': list()
            },
            'Firmware': list(),
            'Ramdisk': list()
        }

        with open('{}/Info.plist'.format(self.bundle), 'rb') as f:
            data = plistlib.load(f)

            # Add our info from the plist to my dict cause easier reading

            if 'org.saurik.cydia' in data['PreInstalledPackages']:
                info['Jailbroken'] = True
            else:
                info['Jailbroken'] = False

            info['RemoveManifest'] = data['DeleteBuildManifest']
            info['IPSWHash'] = data['SHA1']
            info['IPSWName'] = data['Filename']

            info['RootFS']['RootFSFilename'] = data['RootFilesystem']
            info['RootFS']['RootFSSize'] = data['RootFilesystemSize']
            info['RootFS']['RootFSKey'] = data['RootFilesystemKey']
            info['RootFS']['RootFSMountName'] = data['RootFilesystemMountVolume']

            for stuff in data['FilesystemPatches'].items():
                info['RootFS']['Patches'].append(stuff[1])

            for stuff in data['FirmwarePatches'].items():
                info['Firmware'].append(stuff[1])

            for stuff in data['RamdiskPatches'].items():
                info['Ramdisk'].append(stuff[1])

            return info

    def checkForBundle(self, device, version, buildid):
        path = '{}_{}_{}.bundle'.format(device, version, buildid)
        if path in os.listdir('FirmwareBundles'):
            if os.listdir('FirmwareBundles'):
                print('{} exists!'.format(path))
            else:
                print('{} exists but is empty!'.format(path))
        else:
            print('{} does not exist!'.format(path))
