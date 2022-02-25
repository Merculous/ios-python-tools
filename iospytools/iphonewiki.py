
import re
from .remote import downloadFromURL, requestFromURL


class Wiki:
    def __init__(self) -> None:
        self.info = {}

    def readModels(self):
        url = 'https://www.theiphonewiki.com/w/index.php?title=Models&action=edit'
        return requestFromURL(url, True).decode().splitlines()

    def extractTemplate(self, text: list):
        template = {}

        devices = (
            re.compile(r'apple tv', re.IGNORECASE),
            re.compile(r'apple watch', re.IGNORECASE),
            re.compile(r'ipad', re.IGNORECASE),
            re.compile(r'ipod', re.IGNORECASE),
            re.compile(r'iphone', re.IGNORECASE)
        )

        count = 0

        for line in text:

            if line.startswith('== ') and line.endswith(' =='):
                for device in devices:
                    if device.search(line):
                        section = line[5:-5].split('|')
                        template[section[1]] = {
                            'title': section[0],
                            'start': count
                        }

            # FIXME Below is ugly

            if line == '|}':
                if template:
                    template[section[1]]['end'] = count + 1

                    template[section[1]]['length'] = template[section[1]
                                                              ]['end'] - template[section[1]]['start']

                    template[section[1]]['data'] = text[template[section[1]]
                                                        ['start']:template[section[1]]['end']]

            count += 1

        return template
