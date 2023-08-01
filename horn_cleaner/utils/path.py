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

    def files(self):
        if not self.is_dir():
            return None
        files = []
        for element in self.children():
            if element == "meta.json":
                continue
            file = f"{self.__fullpath}/{element}"
            if os.path.isfile(file):
                files.append(file)
        return files

    def folders(self):
        if not self.is_dir():
            return None
        folders = []
        for element in self.children():
            folder = f"{self.__fullpath}/{element}"
            if os.path.isdir(folder):
                folders.append(folder)
        return folders

    def move(self, destination):
        if destination.startswith("../"):
            location = os.path.join('\\'.join(self.path().split('\\')[0:-1]), destination.split("/")[1])
        else:
            location = destination
        print(location)
        print(self.path() + location)
        pathlib.Path(self.fullpath()).rename(location)

    def exists(self):
        return os.path.exists(self.fullpath())

    def name(self):
        return pathlib.Path(self.fullpath()).name

    def path(self):
        return os.path.dirname(self.fullpath())