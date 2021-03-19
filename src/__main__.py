#!/usr/bin/env python3

import sys
from argparse import ArgumentParser

from src.ipswapi import API
from src.tss import TSS


def main() -> None:
    parser = ArgumentParser(
        usage='iospytools <args>',
        description='provides useful commands which are used in iOS research'
    )

    parser.add_argument(
        '-d',
        nargs=1,
        type=str,
        metavar='device'
    )

    parser.add_argument(
        '-e',
        nargs=1,
        type=str,
        metavar='ecid'
    )

    parser.add_argument(
        '-i',
        nargs=1,
        type=str,
        metavar='iOS'
    )

    parser.add_argument(
        '--codename',
        action='store_true',
        help='Get the codename of an iOS (Used with -d and -i)'
    )

    parser.add_argument(
        '--convert',
        action='store_true',
        help='convert an iOS to a buildid (Used with -d and -i)'
    )

    parser.add_argument(
        '--download',
        action='store_true',
        help='Download an ipsw or OTA archive (Used with -d and -i)'
    )

    parser.add_argument(
        '--keys',
        action='store_true',
        help='Get keys for an iOS (Used with -d and -i)'
    )

    parser.add_argument(
        '--path',
        nargs=1,
        type=str,
        metavar='path',
        help='Download a file (used with --download)'
    )

    parser.add_argument(
        '--url',
        action='store_true',
        help='Return the url to an iOS (Used with -d and -i)'
    )

    parser.add_argument(
        '--shsh',
        action='store_true',
        help='Save an shsh blob for a signed iOS (ipsw only atm) (used with -d and -e)'
    )

    parser.add_argument(
        '--signed',
        action='store_true',
        help='Get all currently signed iOS versions, including OTA and beta (can be used with -d)'
    )

    parser.add_argument(
        '--test',
        action='store_true'
    )

    args = parser.parse_args()

    if args.test:
        pass

    elif args.d:

        if args.e and args.shsh:
            t = TSS(args.d[0], args.e[0])
            t.saveBlobs()

        if args.i:
            a = API(args.d[0], args.i[0])

            if args.codename:
                codename = a.getCodename()
                print(codename)

            if args.convert:
                buildid = a.iOSToBuildid()
                print(buildid['buildid'])

            if args.download and not args.path:
                a.downloadArchive()

            elif args.download and args.path:
                a.readFromRemoteArchive(args.path[0], True)

            if args.keys:
                keys = a.getKeys()
                print(keys)

            if args.url:
                url = a.getArchiveURL()
                print(url)

        if args.signed and not args.e:
            a = API(args.d[0])
            versions = a.getSignedVersions()
            print(versions)

    elif args.signed and not args.d:
        a = API()
        versions = a.getSignedVersions()
        print(versions)

    else:
        sys.exit(parser.print_help(sys.stderr))


main()
