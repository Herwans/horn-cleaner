import os
import pathlib
import re

import click

from vulcan.utils import prompt, utils
from vulcan.utils.config import Configuration
from vulcan.utils.path import Path

to_delete = Configuration().get_delete_pattern()


@click.command()
@click.argument("folder")
@click.option("--dry-run", "-d", "dryrun", is_flag=True, default=False, help="Prevent modification")
@click.option("--sub", "-s", is_flag=True, default=False, help="Apply to the folder and it's sub folders")
def garbage(folder, dryrun, sub):
    """Remove empty folders, delete unwanted elements"""

    clean(folder, dryrun)

    if sub:
        for element in Path(folder).folders():
            clean(element, dryrun)
            move(element, dryrun)
            delete(element, dryrun)


def clean(folder, dryrun):
    """Remove elements which match regex to be deleted"""
    for element in Path(folder).files():
        if is_to_delete(element):
            if dryrun is False:
                os.remove(element)
                prompt.alert(f"{element} deleted")
            else:
                prompt.alert(f"{element} is candidate to deletion")


def move(folder, dryrun):
    """Empty folder when no other files nor folders present"""
    path = Path(folder)

    if path.count() == 0 or len(path.folders()) > 0:
        return
    elements = path.files()
    total = path.count()
    videos = 0
    for element in elements:
        if utils.is_video(element):
            videos = videos + 1

    if videos == total:
        if dryrun is False:
            for element in elements:
                current = Path(element)
                if not pathlib.Path(f"{folder}{os.sep}..{os.sep}{current.name()}").exists():
                    current.move(f"..{os.sep}{current.name()}")
            if path.count() == 0:
                prompt.info(f"{folder} has been emptied")
            else:
                prompt.alert(f"{folder} can't be emptied")
        else:
            prompt.info(f"{folder} is candidate to simplification")


def delete(folder, dryrun):
    """Delete folder when empty"""
    path = Path(folder)
    if path.count() == 0:
        if dryrun is False:
            utils.delete_folder(folder)
        else:
            prompt.info(f"{folder} will be deleted")


def is_to_delete(element):
    for pattern in to_delete:
        if re.search(pattern, element) is not None:
            return True
    return False
