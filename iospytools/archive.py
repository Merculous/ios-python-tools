
import os
import zipfile
from typing import Generator


class Archive:
    def __init__(self, path: str) -> None:
        self.path = path

    def info(self) -> dict:
        """Get a dict of the contents of a zip archive with info about each path"""
        if zipfile.is_zipfile(self.path):
            with zipfile.ZipFile(self.path) as f:
                return f.NameToInfo
        else:
            raise zipfile.error(f'{self.path} is not a zip archive!')

    def listContents(self) -> Generator:
        """Extract splitted paths from a zip archive"""
        return (os.path.split(p) for p in self.info())
