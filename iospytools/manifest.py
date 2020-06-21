import plistlib

try:
    from .utils import getDeviceType, getMajorDeviceRevision, getMinorDeviceRevision, fastTokenHex
except ImportError:
    pass


class BuildManifest(object):
    def __init__(self, data):
        super().__init__()

        try:
            stuff = plistlib.loads(data)
        except IOError:
            print('Failed to read manifest!')
            raise
        else:
            self.data = stuff

    def parse(self):
        data = self.data
        return data


class TSSManifest(object):
    def __init__(self):
        super().__init__()

    # Thanks tihmstar! http://blog.tihmstar.net/2017/01/basebandgoldcertid-not-found-please.html
    # https://github.com/tihmstar/tsschecker/blob/master/tsschecker/tsschecker.c#L110

    #  Returns BbGoldCertId, BbSNUM length

    def getBbConfigurationForDevice(self, device):
        if getDeviceType(device) == 'iPhone':
            if getMajorDeviceRevision(device) == 1 \
                    or getMajorDeviceRevision(device) == 2:
                return []

            if getMajorDeviceRevision(device) == 3:
                if getMinorDeviceRevision(device) <= 2:
                    return [257, 12]
                else:
                    return [2, 4]

            if getMajorDeviceRevision(device) == 4:
                return [2, 4]

            if getMajorDeviceRevision(device) == 5:
                if getMinorDeviceRevision(device) <= 2:
                    return [3255536192, 4]
                else:
                    return [3554301762, 4]

            if getMajorDeviceRevision(device) == 6:
                return [3554301762, 4]

            if getMajorDeviceRevision(device) == 7:
                return [3840149528, 4]

            if getMajorDeviceRevision(device) == 8:
                return [3840149528, 4]

            if getMajorDeviceRevision(device) == 9:
                if getMinorDeviceRevision(device) <= 2:
                    return [2315222105, 4]
                else:
                    return [1421084145, 12]

            if getMajorDeviceRevision(device) == 10:
                if getMinorDeviceRevision(device) <= 3:
                    return [2315222105, 4]
                else:
                    return [524245983, 12]

            if getMajorDeviceRevision(device) == 11:
                return [165673526, 12]

            if getMajorDeviceRevision(device) == 12:
                return [524245983, 12]

        if getDeviceType(device) == 'iPad':
            if getMajorDeviceRevision(device) == 1:
                return []

            if getMajorDeviceRevision(device) == 2:
                if getMinorDeviceRevision(device) >= 2 \
                        and getMinorDeviceRevision(device) <= 3:
                    return [257, 12]

                if getMinorDeviceRevision(device) >= 6 \
                        and getMinorDeviceRevision(device) <= 7:
                    return [3255536192, 4]

            if getMajorDeviceRevision(device) == 3:
                if getMinorDeviceRevision(device) >= 2 \
                        and getMinorDeviceRevision(device) <= 3:
                    return [4, 4]

                if getMinorDeviceRevision(device) >= 5:
                    return [3255536192, 4]

            if getMajorDeviceRevision(device) == 4:
                if (getMinorDeviceRevision(device) >= 2
                    and getMinorDeviceRevision(device) <= 3) \
                                                         \
                    or (getMinorDeviceRevision(device) >= 5
                        and getMinorDeviceRevision(device) <= 6) \
                                                         \
                    or (getMinorDeviceRevision(device) >= 8
                        and getMinorDeviceRevision(device) <= 9):
                    return [3554301762, 4]

            if getMajorDeviceRevision(device) == 5:
                if getMinorDeviceRevision(device) == 2 \
                        or getMinorDeviceRevision(device) == 4:
                    return [3840149528, 4]

            if getMajorDeviceRevision(device) == 6:
                if getMinorDeviceRevision(device) == 4 \
                        or getMinorDeviceRevision(device) == 8 \
                        or getMinorDeviceRevision(device) == 11:
                    return [3840149528, 4]

            if getMajorDeviceRevision(device) == 7:
                if getMinorDeviceRevision(device) == 2 \
                        or getMinorDeviceRevision(device) == 4:
                    return [2315222105, 4]

                if getMinorDeviceRevision(device) == 6:
                    return [3840149528, 4]

                if getMinorDeviceRevision(device) == 12:
                    return [524245983, 12]

            if getMajorDeviceRevision(device) == 8:
                if (getMinorDeviceRevision(device) >= 3
                    and getMinorDeviceRevision(device) <= 4) \
                                                         \
                    or (getMinorDeviceRevision(device) >= 7
                        and getMinorDeviceRevision(device) <= 8):
                    return [165673526, 12]

            if getMajorDeviceRevision(device) == 11:
                if getMinorDeviceRevision(device) == 2 \
                        or getMinorDeviceRevision(device) == 4:
                    return [165673526, 12]

        return []

    # See 'Notes' in https://www.theiphonewiki.com/wiki/SHSH_Protocol#Communication
    def createTSSTestVersionManifest(self, path):
        testVersionManifest = dict(
            ApSecurityDomain=1
        )

        with open(path, 'wb+') as v:
            # I'm getting module plistlib has no 'FMT_XML' member error from pylint, according to docs, its supported, guess this is a bug?
            plistlib.dump(testVersionManifest, v, fmt=plistlib.FMT_XML)

    # See 'Sending data (request)' in https://www.theiphonewiki.com/wiki/SHSH_Protocol#Communication
    def initFromBuildManifest(self, device, tss_manifest_path, build_manifest_path, ecid, apnonce='', sepnonce='', bbsnum=''):
        with open(build_manifest_path, 'rb+') as f:
            data = plistlib.load(f, fmt=plistlib.FMT_XML)

            has_baseband = False
            found_erase_identity = False

            # Set TSS manifest to the Erase preset
            for identity in data['BuildIdentities']:
                if 'Erase' in identity['Info']['Variant']:
                    for component in identity['Info']['VariantContents']:
                        if component == 'SEP':  # Set SepNonce now
                            if sepnonce == '':
                                sepnonce = fastTokenHex(20)

                            identity['SepNonce'] = int(
                                sepnonce, 16).to_bytes(20, 'big')

                        elif component == 'BasebandFirmware':  # Enable Baseband-related keys later
                            has_baseband = True

                    # This will clash with the root key labeled 'Info'
                    del identity['Info']

                    data = identity
                    found_erase_identity = True
                    break

            if not found_erase_identity:
                print('No \'Erase\' BuildIdentity was found in the BuildManifest')
                exit(1)

            for key in ['Info', 'ProductMarketingVersion']:  # Remove unnecessary root keys
                try:
                    del data[key]
                except:
                    pass

            # production_mode = False
            # security_mode = False

            for component in data['Manifest']:
                content = data['Manifest'][component]

                #  This is messy; fix later

                if 'RestoreRequestRules' in content['Info']:
                    for rule in content['Info']['RestoreRequestRules']:
                        if 'EPRO' in rule['Actions']:
                            content['EPRO'] = True
                            if 'ApRequiresImage4' in rule['Conditions']:
                                if rule['Conditions']['ApRequiresImage4']:
                                    data['@ApImg4Ticket'] = True

                        elif 'ESEC' in rule['Actions']:
                            content['ESEC'] = True

                if 'Trusted' in content and 'Digest' not in content:
                    content['Digest'] = bytes()

                del content['Info']

                data[component] = content  # Move keys to root

            if '@ApImg4Ticket' not in data:
                data['@APTicket'] = True  # Old IMG3 ticket

            del data['Manifest']

            #  These are hardcoded for now; will change later

            data['ApProductionMode'] = True
            data['ApSecurityMode'] = True

            if has_baseband:
                bb_config = self.getBbConfigurationForDevice(device)
                if bb_config != [] and bbsnum:
                    if 'BbChipID' in data:
                        data['BbChipID'] = int(data['BbChipID'], 16)

                    data['@BBTicket'] = True
                    data['BbGoldCertId'] = bb_config[0]

                    if len(bbsnum) != bb_config[1]:
                        print('Provided BbSNUM length is', len(bbsnum),
                              'while the max for', device, 'is', bb_config[1])
                        exit(1)

                    data['BbSNUM'] = int(bbsnum, 16).to_bytes(
                        bb_config[1], 'big')
                else:
                    print(
                        device, 'either does not have a known BbGoldCertId and/or you have not supplied a BbSNUM. Skipping BBTicket...')
                    for key in list(data):
                        if key == 'BasebandFirmware' or key[0:2] == 'Bb':
                            del data[key]

            if len(ecid) == 13 or len(ecid) == 11:
                try:
                    data['ApECID'] = int(ecid, 16)  # Hex ECID
                except:
                    data['ApECID'] = int(ecid)      # Decimal ECID
            else:
                data['ApECID'] = int(ecid)          # Decimal ECID

            if apnonce == '':
                apnonce = fastTokenHex(20)

            data['ApNonce'] = int(apnonce, 16).to_bytes(20, 'big')

        with open(tss_manifest_path, 'wb+') as p:
            plistlib.dump(data, p, fmt=plistlib.FMT_XML)

        return {
            'apnonce':  apnonce,
            'sepnonce': sepnonce
        }
