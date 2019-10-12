import json
from urllib.parse import urlsplit
from urllib.request import urlopen, Request, urlretrieve


def versionToBuildid(device, version):
    url = f'https://api.ipsw.me/v3/{device}/{version}/buildid'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'})
    data = urlopen(req).read()  # Throws an exception if there are more than one buildid's for an iOS, json is needed?
    buildid = data.decode()  # Must be decoded
    print(buildid)
    # TODO Some how return (print also for debugging for now) the buildid but also use that for downloadIPSW.


def downloadIPSW(device, buildid):
    tmpurl = f'https://api.ipsw.me/v4/ipsw/download/{device}/{buildid}'  # This will point to the api.ipsw.me url only
    realurl = urlopen(tmpurl).geturl()  # This will give the actual Apple ipsw url
    split = urlsplit(realurl)
    filename = split.path.split('/')[-1]  # This just grabs the name of the ipsw from the Apple url
    urlretrieve(realurl, filename)


def grabKeys(device, version):
    url = Request(f'https://api.ipsw.me/v4/keys/ipsw/{device}/{version}', headers={'Accept': 'application/json'})
    response_body = urlopen(url).read()
    print(response_body)
    # TODO If keys are not found, MAYBE use iphonewiki for keys, or even just use iphonewiki only because from before
    # some keys are still missing on ipsw.me Maybe even implement a function that grabs keys with GID from ipwndfu
    # and open a page with proper info. Create a local file or print out contents and just copy and paste to url.