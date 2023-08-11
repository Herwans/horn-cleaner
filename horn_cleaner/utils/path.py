import os
import pathlib
import shutil


class Path:
    def __init__(self, fullpath):
        self.__fullpath = fullpath
        self.__is_dir = os.path.isdir(fullpath)

    def fullpath(self):
        return self.__fullpath

    def is_dir(self):
        return self.__is_dir

    def count(self):
        if not self.is_dir():
            return None
        return len(self.files()) + len(self.folders())

    def children(self):
        if not self.is_dir():
            return None
        return os.listdir(self.fullpath())

    def files(self, no_parent=False):
        if not self.is_dir():
            return None
        files = []
        for element in self.children():
            if element == "meta.json":
                continue
            file = f"{self.__fullpath}{os.sep}{element}"
            if os.path.isfile(file):
                if no_parent:
                    files.append(element)
                else:
                    files.append(file)
        return files

    def folders(self, no_parent=False):
        if not self.is_dir():
            return None
        folders = []
        for element in self.children():
            folder = f"{self.__fullpath}{os.sep}{element}"
            if os.path.isdir(folder):
                if no_parent:
                    folders.append(element)
                else:
                    folders.append(folder)
        return folders

    def move(self, destination):
        if destination.startswith(".." + os.sep):
            location = os.path.join(os.sep.join(self.path().split(os.sep)[0:-1]), destination.split(os.sep)[1])
        else:
            location = destination

        pathlib.Path(self.fullpath()).rename(location)

    def exists(self):
        return os.path.exists(self.fullpath())

    def name(self):
        return pathlib.Path(self.fullpath()).name

    def path(self):
        return os.path.dirname(self.fullpath())