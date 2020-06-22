#!/usr/bin/env python3

"""

This is basically what the frontend is, if that's even correct terminology.

Handles arguments and passes them to the functions.

"""

import argparse
import sys

try:
    # from iospytools.bundle import Bundle
    # from iospytools.foreman import Foreman
    # from iospytools.img3 import IMG3
    # from iospytools.img4 import IMG4
    from iospytools.iphonewiki import iPhoneWiki
    # from iospytools.ipsw import IPSW
    from iospytools.ipswapi import API
    # from iospytools.manifest import BuildManifest
    # from iospytools.template import Template
    # from iospytools.tss import TSS
    from iospytools.utils import splitKbag
    # from iospytools.usb import USB
except ImportError:
    raise


def main():
    """

    Main file to interact with the ipsw.me api and such.
    Some stuff to parse iOS and etc.

    """
    argv = sys.argv

    parser = argparse.ArgumentParser(
        usage='iospytools <option> <args>',
        description='provides useful tools/commands which are used in iOS research')

    parser.add_argument(
        "--buildid",
        help="Convert an iOS to its buildid",
        nargs=2,
        metavar=('DEVICE', 'iOS'))

    parser.add_argument(
        "--codename",
        help="Get the codname of an iOS",
        nargs=2,
        metavar=('DEVICE', 'iOS'))

    parser.add_argument(
        "--download",
        help="Download an IPSW",
        nargs=2,
        metavar=('DEVICE', 'iOS'))

    parser.add_argument(
        "--keys",
        help="Get keys for an iOS",
        nargs=2,
        metavar=('DEVICE', 'iOS'))

    parser.add_argument(
        "--manifest",
        help="Download a Build Manifest from an iOS",
        nargs=2,
        metavar=('DEVICE', 'iOS'))

    parser.add_argument(
        "--shsh",
        help="Save SHSH for all signed iOS versions",
        nargs=2,
        metavar=('DEVICE', 'ECID'))

    parser.add_argument(
        "--signed",
        help="Print the signed iOS versions for a device",
        nargs=1,
        metavar='DEVICE')

    parser.add_argument(
        "--split",
        help="Split a GID decrypted key",
        nargs=1,
        metavar='KEY')

    args = parser.parse_args()

    if args.buildid:  # ./yeet --buildid device iOS
        api = API(argv[2], argv[3])
        print(api.iOSToBuildid())

    elif args.codename:  # ./yeet --codename device iOS
        api = API(argv[2], argv[3])
        print(api.getCodename())

    elif args.download:  # ./yeet --download device iOS
        api = API(argv[2], argv[3])
        api.downloadIPSW()

    elif args.keys:  # ./yeet --keys device iOS (WIP --save)
        wiki = iPhoneWiki(argv[2], argv[3])
        data = wiki.getWikiKeys()
        for stuff in data:
            print(stuff)

    elif args.manifest:  # ./yeet --manifest device iOS
        api = API(argv[2], argv[3])
        api.downloadFileFromArchive('BuildManifest.plist')

    elif args.shsh:  # ./yeet --shsh device ecid
        # tss = TSS(argv[2], argv[3])
        # tss.saveBlobs()
        sys.exit('Sorry :*( Currently working on an update for this. eta s0n?')

    elif args.signed:  # ./yeet --signed device
        api = API(argv[2])
        for stuff in api.getSignedVersions():
            print('{} ({}) {}'.format(
                stuff['iOS'], stuff['buildid'], stuff['filetype']))

    elif args.split:  # ./yeet --split kbag
        kbag = splitKbag(argv[2])
        print('IV:', kbag['iv'])
        print('Key:', kbag['key'])

    else:
        sys.exit(parser.print_help(sys.stderr))


if __name__ == '__main__':
    main()
