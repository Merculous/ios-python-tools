import os
import plistlib
import shutil
from urllib.request import Request, urlopen

from .ipswapi import API
from .manifest import TSSManifest

tss_url = 'https://gs.apple.com/TSS/controller?action=2'

# See https://www.theiphonewiki.com/wiki/SHSH_Protocol#Communication
tss_headers = {
    'User-Agent': 'InetURL/1.0',
    'Proxy-Connection': 'Keep-Alive',
    'Pragma': 'no-cache',
    'Content-type': 'text/xml; charset="utf-8"'
}

# TODO Add support for OTA saving

class TSS:
    def __init__(self, device: str, ecid: str, apnonce='', sepnonce='', bbsnum='', shsh_path='shsh'):
        self.device = device
        self.ecid = ecid
        self.apnonce = apnonce
        self.sepnonce = sepnonce
        self.bbsnum = bbsnum
        self.shsh_path = shsh_path

    def makeTSSRequest(self, data: bytes):
        request = Request(tss_url, headers=tss_headers, data=data)
        response = urlopen(request, timeout=5.0)
        response_text = response.read().decode('utf-8')

        if 'STATUS=0' not in response_text:
            if response.headers['Content-Length'] == '0':
                print('Server returned no response... are you blacklisted?')
            else:
                print(f'Server error: {response_text}')
        else:
            # Remove TSS response header
            return response_text[response_text.find('<?xml'):]

    # TODO Add exception if we can't get a blob for a iOS/buildid

    def saveBlobs(self):
        if os.path.exists('.shsh'):
            shutil.rmtree('.shsh')

        os.mkdir('.shsh')

        if not os.path.exists(self.shsh_path):
            os.mkdir(self.shsh_path)

        tss_test_version_manifest = os.path.join(
            '.shsh', 'TSSTestVersionManifest.plist')

        manobj = TSSManifest()
        manobj.createTSSTestVersionManifest(tss_test_version_manifest)

        #  There is a better way to do the following (likely by using plistlib.loads/dumps)

        print('Sending TSS server version request...')

        with open(tss_test_version_manifest, 'rb') as v:
            tss_version_response = self.makeTSSRequest(v.read())

        with open(tss_test_version_manifest, 'w') as p:
            p.write(tss_version_response)

        with open(tss_test_version_manifest, 'rb') as v:
            tss_version_response = plistlib.load(v, fmt=plistlib.FMT_XML)

        tss_server_version = tss_version_response['@ServerVersion']

        if tss_server_version != '2.1.0':
            print(
                f'WARNING: TSS server version {tss_server_version} may not be supported by this script!')

        a = API(self.device)
        signed_versions = a.getSignedVersions()

        # FIXME I'm sure I can do this better.

        for tmp1 in signed_versions.items():
            version = tmp1[0]
            a.version = version
            for tmp2 in tmp1[1]:
                if tmp2 == 'ipsw':  # FIXME Fix if there's more than one buildid
                    buildid = tmp1[1][tmp2]['buildid'][0]

                    # Copy the manifest inside which will contain the added string

                    build_manifest = f'.shsh/BuildManifest_{self.device}_{version}_{buildid}.plist'
                    tss_manifest = f'.shsh/TSSManifest_{self.device}_{version}_{buildid}.plist'

                    a.readFromRemoteArchive(
                        'BuildManifest.plist', True, '.shsh')
                    shutil.move('.shsh/BuildManifest.plist', build_manifest)

                    print('Converting from BuildManifest to TSS manifest...')
                    apnonce = manobj.initFromBuildManifest(
                        self.device, tss_manifest, build_manifest, self.ecid, apnonce=self.apnonce, sepnonce=self.sepnonce, bbsnum=self.bbsnum)['apnonce']

                    print(f'Sending TSS request for {version} ({buildid})...')

                    with open(tss_manifest, 'rb') as f:
                        tss_response = self.makeTSSRequest(f.read())

                    if tss_response:

                        blob_path = os.path.join(
                            self.shsh_path, f'{self.ecid}_{self.device}_{version}-{buildid}_{apnonce}.shsh2')

                        with open(blob_path, 'w+') as blob:
                            blob.write(tss_response)
                            print(f'Saved {version} blob to {blob_path}')

        shutil.rmtree('.shsh')
