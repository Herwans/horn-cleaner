import os
import click
from horn_cleaner.utils import utils


@click.command()
@click.argument("folder")
@click.option("--delete", "-d", is_flag=True, default=False, help="Delete empty folders")
@click.option("--meta", "-m", is_flag=True, default=False, help="Create meta file, include in apply")
@click.option("--sub", "-s", is_flag=True, default=False, help="Indicate to check the folders inside the indicated folder")
@click.option("--verbose", "-v", is_flag=True, default=False, help="Display the corrupted file name")
def integrity(folder, delete, meta, sub, verbose):
    """Allow to clean folder elements' name"""
    click.echo(f"{folder} folder content will be checked")

    if sub:
        for sub_folder in os.listdir(folder):
            if os.path.isdir(f"{folder}/{sub_folder}"):
                corrupted = check_folder_content(f"{folder}/{sub_folder}", verbose)
                if corrupted > 0:
                    click.secho(f"{sub_folder} contains {corrupted} corrupted images")
    else:
        corrupted = check_folder_content(folder, verbose)
        if corrupted > 0:
            click.secho(f"{folder} contains {corrupted} corrupted images")

    return


def check_folder_content(folder, verbose):
    corrupted = 0

    for file in os.listdir(folder):
        if utils.is_image(f"{folder}/{file}") and utils.is_image_corrupted(f"{folder}/{file}", verbose):
            corrupted = corrupted + 1

    return corrupted
