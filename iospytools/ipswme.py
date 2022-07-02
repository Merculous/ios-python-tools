
import json

from .manifest import parseManifest
from .remote import downloadFile, getURLData
from .utils import choose

from remotezip import RemoteZip



class IPSWAPI:
    base_url = 'https://api.ipsw.me/v4/'

    def __init__(self, session, device=None, version=None, restore_type=None):
        self.session = session
        self.device = device
        self.version = version
        self.restore_type = restore_type

    async def getAllDevices(self):
        url = self.base_url + 'devices'
        return json.loads(await getURLData(self.session, url))

    async def getDeviceInfo(self):
        if self.device:
            if self.restore_type == 'ota' or self.restore_type == 'ipsw':
                url = self.base_url + 'device/' + self.device + f'?type={self.restore_type}'
                return json.loads(await getURLData(self.session, url))
            else:
                raise ValueError('No restore type was passed!')
        else:
            raise ValueError('No device was passed!')


    async def iOSToBuildid(self):
        if self.version:
            self.restore_type = 'ipsw'
            ipsw_firmwares = await self.getDeviceInfo()
            self.restore_type = 'ota'
            ota_firmwares = await self.getDeviceInfo()
            self.restore_type = None

            firmwares = {'ipsw': {}, 'ota': {}}

            for data in ipsw_firmwares['firmwares']:
                ipsw_version = data['version']
                ipsw_buildid = data['buildid']

                if ipsw_version not in firmwares['ipsw']:
                    firmwares['ipsw'][ipsw_version] = []

                if ipsw_buildid not in firmwares['ipsw'][ipsw_version]:
                    firmwares['ipsw'][ipsw_version].append(ipsw_buildid)

            for data in ota_firmwares['firmwares']:
                ota_version = data['version']
                ota_buildid = data['buildid']

                if ota_version not in firmwares['ota']:
                    firmwares['ota'][ota_version] = []

                if ota_buildid not in firmwares['ota'][ota_version]:
                    firmwares['ota'][ota_version].append(ota_buildid)

            buildids = []

            if self.version in firmwares['ipsw']:
                buildid = firmwares['ipsw'][self.version]
                buildid.append('ipsw')
                if buildid not in buildids:
                    buildids.append(buildid)

            if self.version in firmwares['ota']:
                buildid = firmwares['ota'][self.version]
                buildid.append('ota')
                if buildid not in buildids:
                    buildids.append(buildid)

            # TODO Return either 'ipsw' or 'ota' from user specified 'self.restore_type'

            if buildids:
                return buildids
            else:
                ValueError('Something went wrong grabbing buildids!')

        else:
            raise ValueError('No version was passed!')

    async def getArchiveURL(self):
        buildids = await self.iOSToBuildid()
        restore_types = ('ipsw', 'ota')
        
        if len(buildids) == 1:
            buildid = buildids[0][0]
            choice = restore_types[0]
        else:
            choice = await choose('Please select which restore type you\'d like to use\n', restore_types)
            print(f'User selected: {choice}')

            if choice == restore_types[0]:
                buildid = buildids[0][0]
            else:
                choices = buildids[1][:-1]
           
                if len(choices) == 1:
                    print('TODO ADD CODE HERE')
                else:
                    buildid = await choose('Please select which buildid you\'d like to use\n', choices)
                    print(f'User selected: {buildid}')

        self.restore_type = choice
        data = await self.getDeviceInfo()

        for value in data['firmwares']:
            if value['buildid'] == buildid:
                return value['url']

    async def getSignedVersionsForDevice(self):
        if self.device:
            signed = {'ipsw': {}, 'ota': {}}

            self.restore_type = 'ipsw'
            ipsw_data = await self.getDeviceInfo()
            self.restore_type = 'ota'
            ota_data = await self.getDeviceInfo()
            self.restore_type = None

            for data in ipsw_data['firmwares']:
                version = data['version']
                buildid = data['buildid']
                is_signed = data['signed']

                if is_signed:
                    signed['ipsw'][version] = buildid
                
            for data in ota_data['firmwares']:
                version = data['version']
                buildid = data['buildid']
                is_signed = data['signed']

                if is_signed:
                    signed['ota'][version] = buildid

            return signed

        else:
            raise ValueError('No device was passed!')


    async def getAllSignedVersions(self):
        devices = await self.getAllDevices()
        signed = {}
        for device in devices:
            identifier = device['identifier']
            self.device = identifier
            signed_versions = await self.getSignedVersionsForDevice()
            signed[identifier] = signed_versions
        
        return signed

    async def downloadArchive(self):
        url = await self.getArchiveURL()
        await downloadFile(self.session, url)

    async def listArchiveContents(self):
        url = await self.getArchiveURL()
        with RemoteZip(url) as f:
            contents = f.filelist
            for thing in contents:
                print(thing.filename)

    async def readFromArchive(self, path):
        url = await self.getArchiveURL()
        with RemoteZip(url) as f:
            data = f.read(path)
            return data

    async def getChipID(self):
        data = await self.getDeviceInfo()
        return hex(data['cpid'])

    async def getCodename(self):
        data = await self.readFromArchive('BuildManifest.plist')
        info = parseManifest(data, await self.getChipID())
        return info['codename']
