#!/usr/bin/env python3

import os, sys, zipfile, tempfile, shutil
from urllib.request import urlopen, Request, urlretrieve
from clint.textui import progress

#TODO Have user enter pwndfu, enter ipsw path, extract files, import modules from ipwndfu to decrypt with gid key.

def downloadIPSW(device, version):
        url = f'https://api.ipsw.me/v3/{device}/{version}/buildid'
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        data = urlopen(req).read()
        buildid = data.decode() # Not sure if we need to decode this.
        print(buildid)

        realurl = f'https://api.ipsw.me/v4/ipsw/download/{device}/{buildid}'
        print(realurl)

        #TODO Download the ipsw :/ Apparently I'm too dumb right now to get this working lol

#TODO Extract files that have kbags.

def extractIPSW(file):
        if zipfile.is_zipfile(file) == True:
                tmp = tempfile.mkdtemp() # Make temp dir
                print(f'We are using {tmp} as the temp dir')
                with zipfile.ZipFile(file, 'r') as ipsw:
                        ipsw.extractall(tmp)

        else:
                print(f'{file} is not a zip archive')

def splitKbag(str):
        size = len(str)
        if size != 96:
                print(f'Length: {size}')
                sys.exit('String provided is not 96 bytes!')
        else:
                #TODO I know for sure this can be made better. Maybe?
                iv = str[:32]
                key = str[-64:]
                print(f'IV: {iv}')
                print(f'Key: {key}')

def usage(name):
        print(f'Usage: {name} <args> <stuff>')
        print('-d\t\tDownload an ipsw for decrypting')
        print('-s\t\tSplit KBAG key')
        print('-x\t\tExtract IPSW')

if __name__ == '__main__':
        argv = sys.argv
        if len(argv) == 1:
                usage(argv[0])

        if len(argv) > 4:
                sys.exit('We are expecting two arguments but a max of 3!')

        if '-d' in argv:
                downloadIPSW(argv[2], argv[3]) # ./grabkeys.py -d device version

        elif '-s' in argv:
                splitKbag(argv[2]) # ./grabkeys.py -s KBAG

        elif '-x' in argv:
                extractIPSW(argv[2]) # ./grabkeys.py -x IPSW