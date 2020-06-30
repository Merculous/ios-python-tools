class IMG4(object):
    def __init__(self, file):
        super().__init__()

        self.file = file

        """

        Class to parse and interact with Apple's img4 formatted files.

        """

    def printTags(self):
        """
        Print the tags of an img3 file
        """

        with open(self.file, 'rb') as f:
            data = f.read()

            if b'IM4P' in data:
                print('I see a IM4P tag at index:', hex(data.find(b'IM4P')))

        f.close()
