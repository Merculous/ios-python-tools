import json
import os
import random
import subprocess
from shutil import rmtree
from urllib.request import Request, urlopen

from .ipswapi import APIParser
from .manifest import TSSManifest
from .utils import fastTokenHex

class TSS(object):
    def __init__(self, device, ecid, version=False, apnonce=False, sepnonce=False, bbsnum=False, useDFUCollidingNonces=False, shsh_path='shsh'):
        super().__init__()
        self.device = device
        self.ecid = ecid
        self.version = version
        self.apnonce = apnonce
        self.sepnonce = sepnonce
        self.bbsnum = bbsnum
        self.useDFUCollidingNonces = useDFUCollidingNonces
        self.shsh_path = shsh_path

    def saveBlobs(self):
        api = APIParser(self.device, self.version)
        signed_versions = api.signed()
        tss_url = 'http://gs.apple.com/TSS/controller?action=2'

        if os.path.exists('.shsh'):
            rmtree('.shsh')
        os.mkdir('.shsh')

        if not os.path.exists(self.shsh_path):
            os.mkdir(self.shsh_path)

        index = 0
        for version, buildid, install_type in signed_versions:
            if install_type == 'ota':
                continue

            if len(signed_versions) > index and index != 0:
                print()

            index += 1

            # Copy the manifest inside which will contain the added string

            build_manifest = os.path.join('.shsh', f'BuildManifest_{self.device}_{version}_{buildid}.plist')
            tss_manifest =   os.path.join('.shsh', f'TSSManifest_{self.device}_{version}_{buildid}.plist')

            api.buildid = buildid
            api.downloadFileFromArchive('BuildManifest.plist', output=build_manifest)

            if self.apnonce == False:
                apnonce = fastTokenHex(40)
            else: apnonce = self.apnonce

            # TODO: Determine is SEPNonce is even needed for device

            if self.sepnonce == False:
                sepnonce = fastTokenHex(40)
            else: sepnonce = self.sepnonce

            print('Converting from BuildManifest to TSS manifest...')
            manobj = TSSManifest(path=tss_manifest)
            manobj.initFromBuildManifest(self.device, build_manifest, self.ecid, apnonce=apnonce, sepnonce=sepnonce, bbsnum=self.bbsnum)
            os.remove(build_manifest)

            # Hot fix by @mcg29_ Thanks :D
            # with open(manifest, 'w') as n:
            #     n.write(newFile)  # Write modified manifest

            print('Sending TSS request for', version, '(' + buildid + ')...')
            
            headers = {'Host': 'gs.apple.com', 'User-Agent': 'InetURL/1.0', 'Content-type': 'text/xml'}  # See https://www.theiphonewiki.com/wiki/SHSH_Protocol#Communication
            with open(tss_manifest, 'rb') as f:
                request = Request(tss_url, headers=headers, data=f.read())

            response = urlopen(request, timeout=5.0)
            if response.status != 200:
                print('Error code in response:', response.status)

            response_text = response.read().decode('utf-8')
            if 'STATUS=0' not in response_text:
                if response.headers['Content-Length'] == '0':
                    print('Server returned no response... are you blacklisted?')
                else:
                    print('Server error:', response_text)
            else:
                response_text = response_text[response_text.find('<?xml'):]  # Remove TSS response header
                blob_path = os.path.join(self.shsh_path, f'{self.ecid}_{self.device}_{version}-{buildid}_{apnonce}.shsh2')
                with open(blob_path, 'w+') as blob:
                    blob.write(response_text)
                    print('Saved', version, 'blob to', blob_path)

            index += 1

        os.remove(f'{self.device}.json')
        #rmtree('.shsh')

    def saveBlobsWithTSSChecker(self):
        a7_dfu_nonces = [
            "6b83f831a6305ae90d57a78ba8eb9d81e7a9058f",
            "7d7bdc28e5eca36dc5bc20c791850f110dc28269",
            "6b81a2c3cdf87404dee28330f7fcb0ee62c425a1",
            "778282f0cf6e5234446d88ebc5dcfde81f415b57",
            "7ce1657233867e988e1b48988ef98fc28ddf20f5",
            "8b9244eba18e07f3ad9d5eed4f972aa98f0c495e",
            "198365e19ea223bd73ee27faa555ca24ac6ed65d",
            "994bf71da4fd4ba758a8ec6c943a5a610be02edb",
            "ee4b7f9b2d7d41bfde4c8390734a83d63c2fe997",
            "8f760412c8653de657e8ea2352f706de2e9ca85c",
            "63e81aabb8e9e45cc756c347e8cdfd9ae7c796ad",
            "1dedf288afea588e803be0737af7ae5ca87d107f",
            "99a7b1ba5977d6c112717cc208a41785aaa7a313",
            "74f5bbf201cbdcb8a145220fdcc6d82c3ce3a9d8",
            "b05a70468054cfe94251b34b58f28450054f1aa9",
            "93d5c7ba2844327ccb0a2a705fa8bb186021b459",
            "728a82a4bf7246939ea5db839ca782604cd97511",
            "99b5e22d771c0f1c81f70c394e9907993a2db435",
            "f5cce05e81a9be2ef66ec287f692ffdf20b13860"
        ]

        a8_dfu_nonces = [
            "1a965b264168d077ad438546b09204e1d92d2c8b",
            "7ba89ec4cb77a7aa3be826ea55196d333f444cce",
            "b5992dc8a668fd474969111b9b1ff1997cf01bab",
            "14b656ea957a73a54a406c536266c0102e8cac0a",
            "d8befbd5b7c9543b3cc06e1fbfc660486494333f",
            "e456e81cff61251f13f17a183b594d072c603adf",
            "a424cfabe80ab6fac7ab11afe0c36ede4c65476d",
            "44605d9daca26c6211e34d07617104da12bb31e4",
            "e2d4e40384b69685ef50d56c427f99162d93fb81",
            "79febc9d8e400fa1cafa2d94296a11563f3a81f9",
            "031628a41c50425b984b2793d45e60a7fc154f96",
            "2c3eb995241e528dea7952bcbb6a72264a5c6d7f",
            "cc0eb67aabdbb06e8560af9b9be158cceb6b1f01",
            "1af3454a672dda5dac9bcd3a8a76cd9164d0e0a3",
            "0c6ec8eb454c40870cd4ef4d89d8c9ccb81d398c",
            "0a475cf24cc2118e9d639f85951c5892e2a5f92e"
        ]

        unc0ver_nonce = "33ad71ce72c2c1d51482af4c40cd4df5c2fd378e43d230793704f18f314fdc83"  # 0x1111111111111111 // default boot-nonce, used in unc0ver

        api = APIParser(self.device, None)
        for versions in api.signed():

            # TODO Add checks to see if we already have the shsh locally

            if self.device == 'iPhone6,1':
                # For safety, also grab blobs with DFU colliding nonces
                for nonces in a7_dfu_nonces:
                    subprocess.check_output(['tsschecker', '-d', self.device, '-i', versions[0], '-e', self.ecid, '--apnonce', nonces, '-s', '--save-path', self.shsh_path])
            elif self.device == 'iPhone7,2':
                # For safety, also grab blobs with DFU colliding nonces
                for nonces in a8_dfu_nonces:
                    subprocess.check_output(['tsschecker', '-d', self.device, '-i', versions[0], '-e', self.ecid, '--apnonce', nonces, '-s', '--save-path', self.shsh_path])
            elif self.device == 'iPhone11,6':
                # Use unc0ver's custom apnonce
                subprocess.check_output(['tsschecker', '-d', self.device, '-i', versions[0], '-e', self.ecid, '--apnonce', unc0ver_nonce, '-s', '--save-path', self.shsh_path])
            else:
                # No custom apnonce used
                subprocess.check_output(['tsschecker', '-d', self.device, '-i', versions[0], '-e', self.ecid, '-s', '--save-path', self.shsh_path])
