import tempfile
import zipfile
import sys


def extractIPSW(file):
    if zipfile.is_zipfile(file):
        tmp = tempfile.mkdtemp()  # Make temp dir
        print(f'We are using {tmp} as the temp dir')
        with zipfile.ZipFile(file, 'r') as ipsw:
            ipsw.extractall(tmp)
    else:
        print(f'{file} is not a zip archive')


def splitKbag(str):
    size = len(str)
    if size != 96:
        print(f'Length: {size}')
        sys.exit('String provided is not 96 bytes!')
    else:
        # TODO I know for sure this can be made better. Maybe?
        iv = str[:32]
        key = str[-64:]
        print(f'IV: {iv}')
        print(f'Key: {key}')
