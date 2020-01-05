import json
import os
from urllib.request import Request, urlopen, urlretrieve

import ipswapi


def saveblobs(device, ecid):
    signed = ipswapi.signed(device)
    tss = 'http://gs.apple.com/TSS/controller?action=2'

    for version, buildid in signed:
        # Setup shsh folder and copy the manifest inside which will contain the added string

        if os.path.exists('shsh'):
            # shutil.rmtree('shsh')
            pass
        else:
            print('temporary shsh folder does not exist, making the folder...')
            os.mkdir('shsh')

        manifest = f'shsh/BuildManifest_{device}_{version}_{buildid}.plist'

        # Check to see if we need to download a manifest or not

        if os.path.exists(manifest):
            print(f'Cool, found {manifest}')
        else:
            print('Did not find a local manifest, downloading...')

            ipswapi.linksForDevice(device)
            with open(f'{device}.json', 'r') as file:
                data = json.load(file)
                i = 0
                buildidFromJsonFile = data['firmwares'][i]['buildid']
                while buildidFromJsonFile != buildid:
                    i += 1
                    buildidFromJsonFile = data['firmwares'][i]['buildid']

                board = data['boardconfig']

                # This will request a manifest with the ecid key already placed
                url = f'http://api.ineal.me/tss/manifest/{board}/{buildid}'
                urlretrieve(url, manifest)
            file.close()

        print('Changing the ECID string value...')
        # Loop through "manifest", use below (replacing strings, by whatever function...), and write changes back to manifest. Open mode: 'r+' is read/write
        newFile = ''  # New manifest with ecid
        with open(manifest, 'r') as m:
            d = (m.read())
            # Having the four spaces (should be a tab or \t?) is crucial?
            newFile = (d.replace('<string>$ECID$</string>',
                                 f'<integer>{ecid}</integer>'))
        # Hot fix by @mcg29_ Thanks :D
        with open(manifest, 'w+') as n:  # Open manifest and read/write, creates file in missing
            n.write(newFile)  # Write modified manifest
        m.close()
        n.close()

        print('Beginning to start asking TSS for shsh...')
        header = {'User-Agent': 'InetURL/1.0', 'Content-type': 'text/xml'}
        request = Request(url=tss, headers=header,
                          data=manifest.encode('utf-8'))
        response = urlopen(request).read()
        print(response)

    # "Content-type: text/xml; charset=\"utf-8\"" "Expect:"

    # os.remove(f'{device}.json')
