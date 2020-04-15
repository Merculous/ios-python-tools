import os
import plistlib
from secrets import token_bytes

class Manifest(object):  # TODO Add OTA compatibility
    def __init__(self, path='BuildManifest.plist'):
        super().__init__()

        self.path = path

    def extractData(self):
        with open(self.path, 'rb+') as f:  # path will default to BuildManifest.plist, unless user provides custom
            data = plistlib.load(f)
            buildid = data['ProductBuildVersion']
            iOS = data['ProductVersion']
            device = data['SupportedProductTypes'][0]
            codename = data['BuildIdentities'][0]['Info']['BuildTrain']
            files = data['BuildIdentities'][0]['Manifest']

        # TODO Fix parsing manifests with multiple devices. iPhone6,1 10.3.3 'files' gives output of n69 instead of its n51

        info = {
            'device': device,
            'ios': iOS,
            'buildid': buildid,
            'codename': codename,
            'files': files
        }
        return info

    def convertToTSSManifest(self, device, output=False, ecid=False, apnonce=False, sepnonce=False, bbsnum=False):  # See 'Sending data (request)' in https://www.theiphonewiki.com/wiki/SHSH_Protocol#Communication
        with open(self.path, 'rb+') as f:
            data = plistlib.load(f, fmt=plistlib.FMT_XML)

            for identity in data['BuildIdentities']:  # Set TSS manifest to the Erase preset
                if 'Erase' in identity['Info']['Variant']:
                    data = identity
                    break

            for key in ['Info', 'ProductMarketingVersion']:
                try: del data[key]
                except: pass

            for key in data['Manifest']:  # Move components from 'Manifest' to root and remove 'Info' dictionary
                del data['Manifest'][key]['Info']
                data[key] = data['Manifest'][key]
            del data['Manifest']

            for key in ['ApBoardID', 'ApChipID', 'ApSecurityDomain']:  # Force string keys to integer
                try: data[key] = int(data[key], 16)
                except: pass

            data['@ApImg4Ticket'] = True
            data['ApProductionMode'] = True
            data['ApSecurityMode'] = True

            requestBaseband = False
            if 'BbChipID' in data:
                data['BbChipID'] = int(data['BbChipID'], 16)
                requestBaseband = True

            if requestBaseband:
                data['@BBTicket'] = True

                if   'iPhone6' in device: data['BbGoldCertId'] =   3554301762

                elif 'iPhone7' in device    \
                or 'iPhone8' in device: data['BbGoldCertId'] =     3840149528

                elif device == 'iPhone9,1'  \
                or device == 'iPhone9,2':  data['BbGoldCertId'] =  2315222105
                elif device == 'iPhone9,3'  \
                or device == 'iPhone9,4':  data['BbGoldCertId'] =  1421084145

                elif device == 'iPhone10,1' \
                or device == 'iPhone10,2'   \
                or device == 'iPhone10,3': data['BbGoldCertId'] =  2315222105

                elif device == 'iPhone10,4' \
                or device == 'iPhone10,5'   \
                or device == 'iPhone10,6': data['BbGoldCertId'] =  524245983

                elif 'iPhone11' in device: data['BbGoldCertId'] =  165673526
                elif 'iPhone12' in device: data['BbGoldCertId'] =  524245983

                elif device == 'iPad2,6'    \
                or device == 'iPad2,7'      \
                or device == 'iPad3,5'      \
                or device == 'iPad3,6': data['BbGoldCertId'] =     3255536192

                elif device == 'iPad4,2'    \
                or device == 'iPad4,3'      \
                or device == 'iPad4,5'      \
                or device == 'iPad4,6'      \
                or device == 'iPad4,8'      \
                or device == 'iPad4,9': data['BbGoldCertId'] =     3554301762

                elif device == 'iPad5,2'    \
                or device == 'iPad5,4'      \
                or device == 'iPad6,4'      \
                or device == 'iPad6,8'      \
                or device == 'iPad6,11'     \
                or device == 'iPad7,6': data['BbGoldCertId'] =     3840149528

                elif device == 'iPad7,2'    \
                or device == 'iPad7,4': data['BbGoldCertId'] =     2315222105

                elif device == 'iPad7,12': data['BbGoldCertId'] =  524245983

                elif device == 'iPad8,3'    \
                or device == 'iPad8,4'      \
                or device == 'iPad8,7'      \
                or device == 'iPad8,8'      \
                or device == 'iPad11,2'     \
                or device == 'iPad11,4': data['BbGoldCertId'] =    165673526

                else: data['BbGoldCertId'] = 0

                if bbsnum != False: data['BbSNUM'] = int(bbsnum, 16).to_bytes(12, 'big')
                else: data['BbSNUM'] = token_bytes(12)

            for key in data:
                if type(data[key]) is dict and key != 'BasebandFirmware':
                    data[key]['ESEC'] = True
                    data[key]['EPRO'] = True
                    if 'Digest' not in data[key]:
                        data[key]['Digest'] = bytes(0)

            if ecid != False:
                if len(ecid) == 16: data['ApECID'] =   int(ecid)      # Decimal ECID
                elif len(ecid) == 13: data['ApECID'] = int(ecid, 16)  # Hex ECID
            else: data['ApECID'] = 0

            if apnonce != False: data['ApNonce'] =   int(apnonce, 16).to_bytes(40, 'big')
            if sepnonce != False: data['SepNonce'] = int(sepnonce, 16).to_bytes(40, 'big')

        if output == False:  # Overwrite original file
            os.remove(self.path)
            with open(self.path, 'wb+') as p:
                plistlib.dump(data, p, fmt=plistlib.FMT_XML)
        else:
            with open(output, 'wb+') as p:
                plistlib.dump(data, p, fmt=plistlib.FMT_XML)

    def getCodename(self):
        return self.extractData()['codename']  # Always works :D

    def getFilePaths(self):
        return self.extractData()['files']

    def getBasebandVersion(self):
        pass
