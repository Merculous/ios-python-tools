
import time
from urllib.error import HTTPError
from urllib.request import Request, urlopen, urlretrieve

from .utils import showProgress


def requestFromURL(url: str, read: bool):
    req = Request(url)
    try:
        response = urlopen(req, timeout=5.0)
    except HTTPError as e:
        if e.code == 404:
            print('Server returned no response... are you blacklisted?')
        elif e.code == 429:
            print('Server is asking us to slow down...')
            wait = int(e.headers['Retry-After'])
            print(f'Waiting {wait} seconds...')
            time.sleep(wait)
            print('Done sleeping! Trying again...')
            requestFromURL(url, read)
        else:
            print(f'Server error: {e.code}')
    else:
        # Remove TSS response header
        if not read:
            return response
        else:
            return response.read()


def downloadFromURL(url: str):
    name = url.split('/')[-1]
    print(f'Downloading {name} at {url}...')
    urlretrieve(url, name, showProgress)
