import re
# import plistlib

# try:
# from .ipwapi import APIParser
# from .manifest import BuildManifest
# except ImportError:
# raise

"""

This will handle the key template stuff from iphonewiki (webpage)

"""

"""

This is the key template for the key pages. When a page uses this template, it is added to the Key Pages category.

Syntax:

If the device is not an iPhone or a cellular iPad, delete the Baseband parameter.

If the device is an Apple TV (iOS versions), set Version to the marketing version with the internal version in parenthesis.

For each *, *IV, and *Key section, put the file name on the first line. If the item is the Root FS or a ramdisk, remove the .dmg
file extension. If that firmware item does not exist in that firmware, delete its parameter section. If the firmware item is not encrypted,
set *IV to "Not Encrypted" and delete the *Key parameter. If the key/iv is not known, then the KBAG should be added.

For devices such as iPhone 6s that have two sets of files such as N71AP and N71mAP, then a second file can be added underneath
with a "2" at the end of the name. For example, you can have AppleLogo and AppleLogo2 blocks.

For DownloadURL, do not place anything other than URLs to free firmwares hosted on Apple Inc.'s servers. For beta firmwares, delete the parameter.

"""


class Template(object):
    def __init__(self):
        super().__init__()

    def createTemplate(self):
        # TODO Make this, completely scrap the template file I have, prepare for pypi functionality
        # manifest = BuildManifest()
        # data = manifest.extractData()

        # api = APIParser(data['device'], data['ios'])
        # url = api.printURLForArchive()

        # raw_template = [
        # "{{keys",
        # "| Version              = ".format(data['ios']),
        # "| Build                = ".format(data['buildid']),
        # "| Device               = ".format(data['device']),
        # "| Codename             = ".format(data['codename']),
        # "| Baseband             = ",
        # "| DownloadURL          = ".format(url),
        # "| RootFS               = ",
        # "| RootFSKey            = ",
        # "| {}                   = ",
        # "| {}IV                 = ",
        # "| {}Key                = ",
        # "| {}KBAG               = ",
        # "}}"
        # ]
        pass

    # FIXME I know I can make this a little better...

    def parseTemplate(self, string):
        keys = string.split('{{keys')[1].split('}}')[0].splitlines()
        new_list = list(filter(None, keys))  # Remove all ''
        fixed = list()
        for stuff in new_list:
            fix = re.sub(r'\s+', ' ', stuff).strip().replace('| ', '')
            epic_fix = fix.replace(' =', '').split()
            data = {epic_fix[0]: epic_fix[1]}
            fixed.append(data)
        return fixed
