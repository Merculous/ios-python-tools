from urllib.parse import urlsplit
from urllib.request import urlopen, Request, urlretrieve


def downloadIPSW(device, version):
    url = f'https://api.ipsw.me/v3/{device}/{version}/buildid'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    data = urlopen(req).read()
    buildid = data.decode()  # Must be decoded
    print(buildid)

    tmpurl = f'https://api.ipsw.me/v4/ipsw/download/{device}/{buildid}'
    print(tmpurl)

    realurl = urlopen(tmpurl).geturl()
    print(realurl)

    split = urlsplit(realurl)
    filename = split.path.split('/')[-1]
    urlretrieve(realurl, filename)