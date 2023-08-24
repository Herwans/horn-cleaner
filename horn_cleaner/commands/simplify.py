import shutil

import click

from horn_cleaner.utils import utils
from horn_cleaner.utils.path import Path


@click.command()
@click.argument("folder")
@click.option("--apply", "-a", is_flag=True, default=False, help="Apply the change")
@click.option("--sub", "-s", is_flag=True, default=False, help="Apply to the folder and it's sub folders")
def simplify(folder, apply, sub):
    """Remove empty folders, delete unwanted elements"""

    execute(folder, apply)

    if sub:
        for element in Path(folder).folders():
            execute(element, apply)


def execute(folder, apply):
    """When a folder contains only a subfolder with the same name, move the subfolder's content"""
    folder = Path(folder)
    if folder.count() == 1 and len(folder.folders()) == 1:
        subfolder = Path(folder.folders()[0])
        if subfolder.name() == folder.name() and apply:
            for element in subfolder.files():
                shutil.move(element, folder.fullpath())
            for element in subfolder.folders():
                shutil.move(element, folder.fullpath())
            delete(subfolder.fullpath())


def delete(folder):
    """Delete folder when empty"""
    path = Path(folder)
    if path.count() == 0:
        utils.delete_folder(folder)