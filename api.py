import json
import os
from urllib.parse import urlsplit
from urllib.request import urlopen, Request, urlretrieve


def versionToBuildid(device, version):
    url = f'https://api.ipsw.me/v3/{device}/{version}/buildid'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    data = urlopen(req).read()  # Throws an exception if there are more than one buildid's for an iOS, json is needed?
    buildid = data.decode()  # Must be decoded
    return buildid


def downloadIPSW(device, buildid):
    buildid = versionToBuildid(device, buildid)  # First time using my own function in another function :D
    tmpurl = f'https://api.ipsw.me/v4/ipsw/download/{device}/{buildid}'  # This will point to the api.ipsw.me url only
    realurl = urlopen(tmpurl).geturl()  # This will give the actual Apple ipsw url
    split = urlsplit(realurl)
    filename = split.path.split('/')[-1]  # This just grabs the name of the ipsw from the Apple url
    urlretrieve(realurl, filename)


def grabKeys(device, buildid):
    buildid = versionToBuildid(device, buildid)
    url = Request(f'https://api.ipsw.me/v4/keys/ipsw/{device}/{buildid}', headers={'Accept': 'application/json'})
    json_data = urlopen(url).read()
    data = json.loads(json_data)
    with open('keys.json', 'w') as write_file:
        json.dump(data, write_file)
        # print(f'Device: {device}')
        # print(f'Buildid: {buildid}')
        # print(f'File: {filename}')
        # print(f'IV: {iv}')
        # print(f'Key: {key}')

    # os.remove('keys.json')
