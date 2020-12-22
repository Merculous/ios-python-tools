#!/usr/bin/env python3

"""

This is basically what the frontend is, if that's even correct terminology.

Handles arguments and passes them to the functions.

"""

import sys
from argparse import ArgumentParser

sys.path.append('src')

try:
    from api import API
    # from bundle import Bundle
    import diff
    # from foreman import Foreman
    from img3 import IMG3
    # from img4 import IMG4
    from iphonewiki import Wiki
    # from ipsw import IPSW
    # from manifest import BuildManifest
    # from template import Template
    from tss import TSS
    from utils import splitKbag
    # from usb import USB
except ImportError:
    raise


def main() -> None:
    """

    Main file to interact with the ipsw.me api and such.
    Some stuff to parse iOS and etc.

    """

    parser = ArgumentParser(
        usage='iospytools <args>',
        description='provides useful tools/commands which are used in iOS research'
    )

    parser.add_argument('-d', nargs=1, type=str, metavar='\b', help='Device')
    parser.add_argument('-i', nargs=1, type=str, metavar='\b', help='iOS')

    parser.add_argument('-o', action='store_true', help='OTA')
    parser.add_argument('-b', action='store_true', help='Beta')

    parser.add_argument('--buildid', nargs=1, type=str, metavar='\b')

    args = parser.parse_args()

    if args.d:
        if args.i:
            a = API(args.d[0], args.i[0])
            data = a.getArchiveURL()
            oof = ''
    else:
        sys.exit(parser.print_help(sys.stderr))


main()  # Call main no matter what so that I can debug and also call from this file
