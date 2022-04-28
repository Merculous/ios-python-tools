#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import aiohttp
import asyncio
import sys

from argparse import ArgumentParser

from .ipswme import IPSWAPI


def printUsage() -> None:
    print('Usage: iospytools <command> [<args>]')
    sys.exit(1)


async def main(args: tuple) -> None:
    argc = len(args)

    parser = ArgumentParser()
    parser.add_argument('-a', help='all', action='store_true')
    parser.add_argument('-b', help='buildid', nargs='?', const=True)
    parser.add_argument('-d', help='device', nargs='?', const=True)
    parser.add_argument('-i', help='info', action='store_true')
    parser.add_argument('-s', help='signed', action='store_true')
    parser.add_argument('-v', help='version', nargs='?', const=True)
    parser.add_argument('-o', help='ota', action='store_true')
    pargs = parser.parse_args()

    if argc == 1:
        printUsage()

    if pargs.d:  # -d
        async with aiohttp.ClientSession() as session:
            api = IPSWAPI(session)
            if pargs.a and not pargs.i:  # -d -a
                devices = await api.getAllDevices()
                for device in devices:
                    name = device['name']
                    ident = device['identifier']
                    board = device['boardconfig']
                    print(f'{name}: {ident}, {board}')
            elif pargs.i:  # -d <input> -i
                api.device = pargs.d
                info = await api.getDeviceInfo()
                if pargs.a:  # -d <input> -i -a
                    firmwares = info['firmwares']
                    for firmware in firmwares:
                        iOS = firmware['version']
                        buildid = firmware['buildid']
                        url = firmware['url']
                        filesize = firmware['filesize']
                        hash = firmware['sha256sum']
                        signed = firmware['signed']
                        print(f'iOS: {iOS}')
                        print(f'BuildID: {buildid}')
                        print(f'URL: {url}')
                        print(f'Filesize: {filesize}')
                        print(f'SHA256: {hash}')
                        print(f'Signed: {signed}')
                        print('\n')
                elif pargs.v:  # -d <input> -i -v
                    pass

asyncio.run(main(tuple(sys.argv)))
