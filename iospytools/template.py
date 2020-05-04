import re

try:
    from .manifest import BuildManifest
except ImportError as error:
    print('Oof, got error:', error)
    raise

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
        # Basically, "{{keys" + list of strings with "| <name> = <data> + IV, Key, KBAG" + "}}"
        start = "{{keys"
        data = list()
        end = "}}"

        tempate = " ".join([start, end])

        return tempate

    def parseTemplate(self):
        with open('key-template-img3.txt') as f:  # Will need to add some comparisons for img4
            data = f.read()
            keys = data.split('{{keys')[1].split('}}')[0].splitlines()
            new_list = list(filter(None, keys))  # Remove all ''
            fixed = list()
            for stuff in new_list:
                fix = re.sub('\s+', ' ', stuff).strip()
                fixed.append(fix)
            return fixed
        f.close()

    def addManifestData(self):
        template_data = self.parseTemplate()
        manifest = BuildManifest()
        manifest_data = manifest.extractData()

        new_data = list()

        version = ' '.join((template_data[0], manifest_data['ios']))
        buildid = ' '.join((template_data[1], manifest_data['buildid']))
        device = ' '.join((template_data[2], manifest_data['device']))
        codename = ' '.join((template_data[3], manifest_data['codename']))
        #version = ' '.join((template_data[4], manifest_data['baseband']))
        #version = ' '.join((template_data[5], manifest_data['downloadurl']))

        print(template_data)
        new_data.extend([version, buildid, device, codename])
        print(manifest_data)
        print(new_data)

        # TODO Figure out a way to not have to declare all of this.

        # for i in range(6, len(template_data)):
        # print(template_data[i])

        # Within the list, we can just get the name and its index, the next three (or next for RootFS) will be its "data"
