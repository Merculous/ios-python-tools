#!/usr/bin/env python3

import os, sys, zipfile, tempfile, json
from urllib.request import urlopen

#TODO Have user enter pwndfu, enter ipsw path, extract files, use ipwndfu module to decrypt with gid key.

#TODO Extract files that have kbags.

def downloadIPSW(version):
        header = {'Accept': 'application/json'}
        url = 'https://api.ipsw.me/v4/ipsw/' + version
        request = urlopen(url)
        data = json.load(request)
        print(data)

def extractIPSW(file):
        if zipfile.is_zipfile(file) == True:
                tmp = tempfile.mkdtemp() # Make temp dir
                print("We are using %s as the temp dir" % tmp)
                with zipfile.ZipFile(file, 'r') as ipsw:
                        ipsw.extractall(tmp)
        else:
                print("%s is not a zip archive" % file)

def splitKbag(str):
        if len(str) != 96:
                print("Length: %d" % len(str))
                sys.exit("String provided is not 96 bytes!")
        else:
                #TODO I know for sure this can be made better. Maybe?
                iv = str[:32]
                key = str[-64:]
                print("IV: %s" % iv)
                print("Key: %s" % key)

def usage(name):
        print('Usage: %s <args> <stuff>' % name)
        print('-d\t\tDownload an ipsw for decrypting')
        print('-s\t\tSplit KBAG key')
        print('-x\t\tExtract IPSW')

if __name__ == '__main__':
        argv = sys.argv
        if len(argv) == 1:
                usage(argv[0])

        if len(argv) > 4:
                sys.exit("We are expecting two arguments but a max of 3!")

        if '-d' in argv:
                downloadIPSW(argv[2]) # ./grabkeys.py -d version

        elif '-s' in argv:
                splitKbag(argv[2]) # ./grabkeys.py -s KBAG

        elif '-x' in argv:
                extractIPSW(argv[2]) # ./grabkeys.py -x IPSW