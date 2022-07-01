
import itertools

class DIFF:
    def __init__(self, file1, file2):
        self.file1 = file1
        self.file2 = file2

    def diff(self):
        differences = {}

        with open(self.file1, 'rb') as f:
            data1 = f.read()

        with open(self.file2, 'rb') as ff:
            data2 = ff.read()

        x = 0

        for i, ii in itertools.zip_longest(data1, data2):
            if i is None:
                i = 0

            if ii is None:
                ii = 0

            i = hex(i)
            ii = hex(ii)

            if i != ii:
                differences[hex(x)] = (i, ii)

            x += 1

        return differences

    def patch(self):
        pass
