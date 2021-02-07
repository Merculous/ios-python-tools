#!/usr/bin/env python3

import sys
from argparse import ArgumentParser

from src.ipswapi import API


def main() -> None:
    parser = ArgumentParser(
        usage='iospytools <args>',
        description='provides useful commands which are used in iOS research'
    )

    parser.add_argument('--test', action='store_true')

    args = parser.parse_args()

    if args.test:
        a = API('iPhone6,1', '10.3.3')
        stuff = a.iOSToBuildid()
        oof = ''
    else:
        sys.exit(parser.print_help(sys.stderr))


main()
