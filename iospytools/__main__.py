#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import aiohttp
import asyncio
import sys

from .ipswme import IPSWAPI

def printUsage() -> None:
    print('Usage: iospytools <command> [<args>]')
    sys.exit(1)


async def main(args: tuple) -> None:
    argc = len(args)

    async with aiohttp.ClientSession() as session:
        api = IPSWAPI(session)
        devices = await api.getAllDevices()
        print(devices)

asyncio.run(main(tuple(sys.argv)))
