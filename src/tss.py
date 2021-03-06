import os
import plistlib
import shutil
from urllib.request import Request, urlopen

try:
    from api import API
    from manifest import TSSManifest
except ImportError:
    raise

tss_url = 'https://gs.apple.com/TSS/controller?action=2'
tss_headers = {'User-Agent': 'InetURL/1.0', 'Proxy-Connection': 'Keep-Alive', 'Pragma': 'no-cache',
               'Content-type': 'text/xml; charset="utf-8"'}  # See https://www.theiphonewiki.com/wiki/SHSH_Protocol#Communication


class TSS(object):
    def __init__(self, device: str, ecid: str, version='', buildid='', apnonce='', sepnonce='', bbsnum='', shsh_path='shsh'):
        super().__init__()
        self.device = device
        self.ecid = ecid
        self.version = version
        self.buildid = buildid
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
                print('Server error: {}'.format(response_text))
        else:
            # Remove TSS response header
            return response_text[response_text.find('<?xml'):]

    def saveBlobs(self):
        api = API(self.device, self.version)
        signed_versions = api.getSignedVersions()

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
            print('WARNING: TSS server version {} may not be supported by this script!'.format(
                tss_server_version))

        for stuff in signed_versions:
            version = stuff['iOS']
            buildid = stuff['buildid']

            oof = API(self.device, version)

            # Copy the manifest inside which will contain the added string

            build_manifest = '.shsh/BuildManifest_{}_{}_{}.plist'.format(
                self.device, version, buildid)
            tss_manifest = '.shsh/TSSManifest_{}_{}_{}.plist'.format(
                self.device, version, buildid)

            oof.downloadFileFromArchive('BuildManifest.plist', '.shsh')
            shutil.move('.shsh/BuildManifest.plist', build_manifest)

            print('Converting from BuildManifest to TSS manifest...')
            apnonce = manobj.initFromBuildManifest(
                self.device, tss_manifest, build_manifest, self.ecid, apnonce=self.apnonce, sepnonce=self.sepnonce, bbsnum=self.bbsnum)['apnonce']

            print('Sending TSS request for {} ({})...'.format(version, buildid))

            with open(tss_manifest, 'rb') as f:
                tss_response = self.makeTSSRequest(f.read())

            blob_path = os.path.join(self.shsh_path, '{}_{}_{}-{}_{}.shsh2'.format(
                self.ecid, self.device, version, buildid, apnonce))
            with open(blob_path, 'w+') as blob:
                blob.write(tss_response)
                print('Saved {} blob to {}'.format(version, blob_path))

        shutil.rmtree('.shsh')
