import click

from horn_cleaner.utils import prompt, utils
from horn_cleaner.utils.config import Configuration
from horn_cleaner.utils.path import Path

@click.command()
@click.argument("folder")
def detect(folder):
    """Detect when elements have the same name after cleaning"""
    folder = Path(folder)

    duplicate_folders = {}
    duplicate_files = {}

    for subfolder in folder.folders(True):
        cleaned = utils.apply_folder_rules(subfolder)
        if cleaned not in duplicate_folders.keys():
            duplicate_folders[cleaned] = []
        duplicate_folders[cleaned].append(subfolder)

    for file in folder.files(True):
        cleaned = utils.apply_file_rules(file)
        if cleaned not in duplicate_folders.keys():
            duplicate_folders[cleaned] = []
        duplicate_folders[cleaned].append(file)

    for title, elements in duplicate_folders.items():
        if len(elements) > 1:
            prompt.info(title)
            for element in elements:
                prompt.info("> " + element)

    for title, elements in duplicate_files.items():
        if len(elements) > 1:
            prompt.info(title)
            for element in elements:
                prompt.info("> " + element)