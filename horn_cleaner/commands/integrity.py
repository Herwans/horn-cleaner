import json
import os
import pathlib
import shutil
from datetime import datetime

import click
from horn_cleaner.utils import utils, prompt


@click.command()
@click.argument("folder")
@click.option("--delete", "-d", is_flag=True, default=False, help="Delete fully corrupted folders")
@click.option("--sub", "-s", is_flag=True, default=False, help="Apply to the folder and it's sub folders")
@click.option("--verbose", "-v", is_flag=True, default=False, help="Display the corrupted file name")
def integrity(folder, delete, sub, verbose):
    """Check file integrity"""
    click.echo(f"{folder} folder content will be checked")

    if sub:
        for sub_folder in os.listdir(folder):
            path = f"{folder}/{sub_folder}"
            if os.path.isdir(path):
                corrupted, total = check_folder_content(path, verbose)
                if corrupted > 0:
                    prompt.line(f"{sub_folder} contains {corrupted} corrupted images ({corrupted / total * 100 }%)")
                    if delete and corrupted == total:
                        if delete_corrupted_folder(path, corrupted, total):
                            prompt.line(f"{sub_folder} deleted")
                        else:
                            prompt.line(f"{sub_folder} kept")
    else:
        corrupted, total = check_folder_content(folder, verbose)
        if corrupted > 0:
            prompt.line(f"{folder} contains {corrupted} corrupted images ({corrupted / total * 100 }%)")
            if delete and corrupted == total:
                if delete_corrupted_folder(folder, corrupted, total):
                    prompt.line(f"{folder} deleted")
                else:
                    prompt.line(f"{folder} kept")

    return


def check_folder_content(folder, verbose):
    corrupted = 0
    total_files = 0
    for file in os.listdir(folder):
        if file == "meta.json":
            continue
        total_files = total_files + 1
        if utils.is_image(f"{folder}/{file}") and utils.is_image_corrupted(f"{folder}/{file}", verbose):
            corrupted = corrupted + 1

    return corrupted, total_files


def delete_corrupted_folder(folder, corrupted, total):
    for element in os.listdir(folder):
        if element != "meta.json" and utils.is_image(element) is False and os.path.isfile(element) is False:
            prompt.alert(element)
            return False
    meta = f"{folder}/meta.json"
    metas = f"{pathlib.Path.home()}/.horn/meta_delete.json"

    if os.path.exists(metas):
        with open(metas, 'r') as f:
            metadatas = json.load(f)
    else:
        metadatas = []

    if os.path.exists(meta):
        with open(meta, 'r') as f:
            metadata = json.load(f)
    else:
        metadata = {"original_name": folder}

    metadata["corruption"] = corrupted / total * 100
    metadata["deleted_at"] = datetime.now().__str__()

    metadatas.append(metadata)
    with open(metas, "w") as f:
        json.dump(metadatas, f)

    shutil.rmtree(folder)
    return True
