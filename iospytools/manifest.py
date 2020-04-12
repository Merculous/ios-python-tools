import os
import plistlib

from .utils import getDeviceType, getMajorDeviceRevision, getMinorDeviceRevision

class BuildManifest(object):
    def __init__(self, path='BuildManifest.plist'):
        super().__init__()

        self.path = path
        with open(self.path, 'rb+') as f:
            self.data = plistlib.load(f)

    def extractData(self):
        return {
            'devices':  self.getDevices(),
            'ios':      self.getVersion(),
            'buildid':  self.getBuildID(),
            'codename': self.getCodename(),
            'files':    self.getFilePaths()
        }

    def getDevices(self):
        return self.data['SupportedProductTypes']

    def getVersion(self):
        return self.data['ProductVersion']

    def getBuildID(self):
        return self.data['ProductBuildVersion']

    def getCodename(self):
        return self.data['BuildIdentities'][0]['Info']['BuildTrain']

    def getFilePaths(self):
        files = list()
        for component in data['BuildIdentities'][0]['Manifest']:
            files.append(component['Info']['Path'])
        
        return files

    def getBasebandVersion(self):
        pass

class TSSManifest(object):
    def __init__(self, path):
        super().__init__()

        self.path = path

    # Thanks tihmstar! http://blog.tihmstar.net/2017/01/basebandgoldcertid-not-found-please.html
    # https://github.com/tihmstar/tsschecker/blob/master/tsschecker/tsschecker.c#L110

    def getBbGoldCertIdForDevice(self, device):
        if getDeviceType(device) == 'iPhone':
            if getMajorDeviceRevision(device) == 1 \
            or getMajorDeviceRevision(device) == 2:
                return -1

            if getMajorDeviceRevision(device) == 3:
                if getMinorDeviceRevision(device) <= 2:
                    return 257
                else:
                    return 2

            if getMajorDeviceRevision(device) == 4: 
                return 2

            if getMajorDeviceRevision(device) == 5:
                if getMinorDeviceRevision(device) <= 2:
                    return 3255536192
                else:
                    return 3554301762

            if getMajorDeviceRevision(device) == 6:
                return 3554301762

            if getMajorDeviceRevision(device) == 7:
                return 3840149528

            if getMajorDeviceRevision(device) == 8:
                return 3840149528

            if getMajorDeviceRevision(device) == 9:
                if getMinorDeviceRevision(device) <= 2:
                    return 2315222105
                else:
                    return 1421084145

            if getMajorDeviceRevision(device) == 10:
                if getMinorDeviceRevision(device) <= 3:
                    return 2315222105
                else:
                    return 524245983

            if getMajorDeviceRevision(device) == 11:
                return 165673526

            if getMajorDeviceRevision(device) == 12:
                return 524245983

        if getDeviceType(device) == 'iPad':
            if getMajorDeviceRevision(device) == 1:
                return -1

            if getMajorDeviceRevision(device) == 2:
                if  getMinorDeviceRevision(device) >= 2 \
                and getMinorDeviceRevision(device) <= 3:
                    return 257

                if  getMinorDeviceRevision(device) >= 6 \
                and getMinorDeviceRevision(device) <= 7:
                    return 3255536192

            if getMajorDeviceRevision(device) == 3:
                if  getMinorDeviceRevision(device) >= 2 \
                and getMinorDeviceRevision(device) <= 3:
                    return 4

                if  getMinorDeviceRevision(device) >= 5:
                    return 3255536192

            if getMajorDeviceRevision(device) == 4:
                if  (getMinorDeviceRevision(device) >= 2 \
                and getMinorDeviceRevision(device) <= 3) \
                                                         \
                or  (getMinorDeviceRevision(device) >= 5 \
                and getMinorDeviceRevision(device) <= 6) \
                                                         \
                or  (getMinorDeviceRevision(device) >= 8 \
                and getMinorDeviceRevision(device) <= 9):
                    return 3554301762

            if getMajorDeviceRevision(device) == 5:
                if  getMinorDeviceRevision(device) == 2 \
                or  getMinorDeviceRevision(device) == 4:
                    return 3840149528

            if getMajorDeviceRevision(device) == 6:
                if  getMinorDeviceRevision(device) == 4 \
                or  getMinorDeviceRevision(device) == 8 \
                or  getMinorDeviceRevision(device) == 11:
                    return 3840149528

            if getMajorDeviceRevision(device) == 7:
                if  getMinorDeviceRevision(device) == 2 \
                or  getMinorDeviceRevision(device) == 4:
                    return 2315222105

                if  getMinorDeviceRevision(device) == 6:
                    return 3840149528

                if  getMinorDeviceRevision(device) == 12:
                    return 524245983

            if getMajorDeviceRevision(device) == 8:
                if  (getMinorDeviceRevision(device) >= 3 \
                and getMinorDeviceRevision(device) <= 4) \
                                                         \
                or  (getMinorDeviceRevision(device) >= 7 \
                and getMinorDeviceRevision(device) <= 8):
                    return 165673526

            if getMajorDeviceRevision(device) == 11:
                if  getMinorDeviceRevision(device) == 2 \
                or  getMinorDeviceRevision(device) == 4:
                    return 165673526

        return 0

    def initFromBuildManifest(self, device, build_manifest_path, ecid, apnonce=False, sepnonce=False, bbsnum=False):  # See 'Sending data (request)' in https://www.theiphonewiki.com/wiki/SHSH_Protocol#Communication
        with open(build_manifest_path, 'rb+') as f:
            data = plistlib.load(f, fmt=plistlib.FMT_XML)

            found_erase_identity = False
            for identity in data['BuildIdentities']:  # Set TSS manifest to the Erase preset
                if 'Erase' in identity['Info']['Variant']:
                    data = identity
                    found_erase_identity = True
                    break

            if found_erase_identity == False:
                raise NoEraseBuildIdentityError('No \'Erase\' BuildIdentity was found in the BuildManifest')

            for key in ['Info', 'ProductMarketingVersion']:
                try: del data[key]
                except: pass

            for key in data['Manifest']:  # Move components from 'Manifest' to root and remove 'Info' dictionary
                del data['Manifest'][key]['Info']
                data[key] = data['Manifest'][key]
            del data['Manifest']

            for key in ['ApBoardID', 'ApChipID', 'ApSecurityDomain']:  # Force string keys to integer
                try: data[key] = int(data[key], 16)
                except:
                    raise RequiredBuildManifestKeyMissingError('The required key \'' + key + '\' is missing from the BuildManifest')

            data['ApProductionMode'] = True

            BbGoldCertId = self.getBbGoldCertIdForDevice(device)
            if bbsnum != False and BbGoldCertId != -1:
                if 'BbChipID' in data:
                    data['BbChipID'] = int(data['BbChipID'], 16)

                data['@BBTicket'] =    True
                data['BbGoldCertId'] = BbGoldCertId
                data['BbSNUM'] = int(bbsnum, 16).to_bytes(12, 'big')
            else:
                for key in list(data):
                    if 'Bb' in key or key == 'BasebandFirmware':
                        del data[key]

            if   len(ecid) == 16 or len(ecid) == 14: data['ApECID'] = int(ecid)      # Decimal ECID
            elif len(ecid) == 13 or len(ecid) == 11: data['ApECID'] = int(ecid, 16)  # Hex ECID
            else:
                raise InvalidECIDLengthError('The ECID \'' + ecid + '\' could not be interpreted')

            if apnonce != False: data['ApNonce'] = int(apnonce, 16).to_bytes(40, 'big')

            # The following devices have an A7, therefore...
            #   * They will use IMG4
            #   * They have SEP

            if ('iPhone'  in device and getMajorDeviceRevision(device) >= 6) \
            or ('iPad'    in device and getMajorDeviceRevision(device) >= 4 and getMinorDeviceRevision(device) >= 4) \
            or ('iPod'    in device and getMajorDeviceRevision(device) >= 7) \
            or ('AppleTV' in device and getMajorDeviceRevision(device) >= 5):
                if sepnonce != False:
                    data['SepNonce'] = int(sepnonce, 16).to_bytes(40, 'big')

                for key in data:
                    if type(data[key]) is dict and key != 'BasebandFirmware':
                        data[key]['ESEC'] = True
                        data[key]['EPRO'] = True
                        if 'Digest' not in data[key]:
                            data[key]['Digest'] = bytes(0)

                data['ApSecurityMode'] = True
                data['@ApImg4Ticket'] =  True
            else:
                data['@APTicket'] = True

        with open(self.path, 'wb+') as p:
            plistlib.dump(data, p, fmt=plistlib.FMT_XML)