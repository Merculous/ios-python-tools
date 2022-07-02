
from hashlib import sha256
from zipfile import ZipFile

class Archive:
    def __init__(self, path: str) -> None:
        self.path = path

    def getSHA256(self):
        with open(self.path, 'rb') as f:
            return sha256(f.read()).hexdigest()
        
    def listContents(self):
        with ZipFile(self.path) as f:
            contents = f.filelist
            for content in contents:
                print(content.filename)

    def createArchive(self, contents):
        pass


    def extract(self, member=None, out_path=None):
        if member:
            with ZipFile(self.path) as f:
                if out_path:
                    f.extract(member, out_path)
                else:
                    f.extract(member)
        else:
            with ZipFile(self.path) as f:
                if out_path:
                    f.extractall(out_path)
                else:
                    f.extractall()
