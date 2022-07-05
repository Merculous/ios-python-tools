
import json

from remotezip import RemoteZip

from .iphonewiki import WIKI
from .manifest import parseManifest
from .remote import downloadFile, getURLData
from .utils import choose


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
                if buildid not in buildids:
                    buildids.append(buildid)

            if self.version in firmwares['ota']:
                buildid = firmwares['ota'][self.version]
                if buildid not in buildids:
                    buildids.append(buildid)

            if buildids:
                if len(buildids) == 1:
                    if len(buildids[0]) == 1: # 1 ipsw value
                        return buildids[0][0]
                    else: # 2 ipsw values
                        choice = await choose('Please select a buildid...\n', buildids[0])
                        print(f'User selected: {choice}')
                        return choice
                elif len(buildids) == 2: # ipsw and ota values
                    restore_types = ('ipsw', 'ota')
                    selected_type = await choose('Please selected a restore type...\n', restore_types)
                    print(f'User selected: {selected_type}')
                    if selected_type == restore_types[0]: # ipsw
                        values = buildids[0]
                        if len(values) == 1:
                            return (values[0], restore_types[0])
                        else:
                            choice = await choose('Please select a buildid...\n', values)
                            print(f'User selcted: {choice}')
                            return (choice, restore_types[0])
                    elif selected_type == restore_types[1]: # ota
                        values = buildids[1]
                        if len(values) == 1:
                            return (values[0], restore_types[1])
                        else:
                            choice = await choose('Please select a buildid...\n', values)
                            print(f'User selected: {choice}')
                            return (choice, restore_types[1])
                else:
                    print('Somehow we got here???')
     
            else:
                ValueError('Something went wrong grabbing buildids!')
        else:
            raise ValueError('No version was passed!')

    async def getArchiveURL(self):
        buildid = await self.iOSToBuildid()
        
        if isinstance(buildid, str):
            build = buildid
            self.restore_type = 'ipsw'
            data = await self.getDeviceInfo()

        elif isinstance(buildid, tuple):
            build = buildid[0]
            self.restore_type = buildid[1]
            data = await self.getDeviceInfo()

        
        for value in data['firmwares']:
            if value['buildid'] == build:
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
            return (url, f.filelist)

    async def readFromArchive(self, path):
        url = await self.getArchiveURL()
        if url:
            with RemoteZip(url) as f:
                data = f.read(path)
                return data
        else:
            raise ValueError('No url was found!')

    async def readFromBuildManifest(self):
        contents = await self.listArchiveContents()
        for line in contents[1]:
            if 'BuildManifest.plist' in line.filename:
                with RemoteZip(contents[0]) as f:
                    data = f.read(line.filename)
                    return data

    async def getBoardConfig(self):
        data = await self.getDeviceInfo()
        return data['boardconfig']

    async def getChipID(self):
        data = await self.getDeviceInfo()
        return hex(data['cpid'])

    async def getCodename(self):
        data = await self.readFromBuildManifest()
        info = await parseManifest(data, await self.getChipID(), await self.getBoardConfig())
        return info['codename']

    async def getKeysFromWiki(self):
        info = await parseManifest(await self.readFromBuildManifest(), await self.getChipID(), await self.getBoardConfig())
        w = WIKI(self.session, info['codename'], info['buildid'], self.device)
        keys = await w.parseTemplate()
        return keys
