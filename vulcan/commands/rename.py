import os
import click
from vulcan.utils import utils, prompt
from vulcan.utils.path import Path


@click.command()
@click.argument("folder")
@click.option("--apply", "-a", is_flag=True, default=False, help="When enable, apply modification")
@click.option("--meta", "-m", is_flag=True, default=False, help="Create meta file, include in apply")
@click.option("--no-meta", "-n", is_flag=True, default=False, help="Prevent meta file creation for file")
@click.option("--delete", "-d", is_flag=True, default=False, help="Delete empty folders")
def rename(folder, apply, meta, no_meta, delete):
    """Allow to clean folder elements' name"""
    prompt.line(f"{folder} folder content will be clean")
    current = Path(folder)
    prompt.line(f"{current.count()} elements have been found")

    change = 0
    skip = 0
    error = 0
    delete_fail = []
    ignore = 0
    remove = 0

    for file in current.files(True):
        if os.path.splitext(file)[1] == ".json":
            ignore = ignore + 1
            continue

        new_file_name = utils.apply_file_rules(file)

        path = f"{folder}/{file}"
        new_path = f"{folder}/{new_file_name}"

        if os.path.exists(new_path):
            skip = skip + 1
        elif new_file_name != file:
            prompt.info("=====================")
            prompt.info("Old : \t" + file)
            prompt.info("New : \t" + new_file_name)

            if apply:
                os.rename(path, new_path)
                if os.path.exists(path) is False and os.path.exists(new_path):
                    change = change + 1
                else:
                    error = error + 1
        if (apply and not no_meta) or meta:
            utils.create_meta_file(folder, file, new_file_name)

    for fol in current.folders(True):
        if apply and delete and utils.delete_folder(fol):
            remove = remove + 1
            continue

        new_folder_name = utils.apply_folder_rules(fol)
        path = f"{folder}/{fol}"
        new_path = f"{folder}/{new_folder_name}"

        if os.path.exists(new_path):
            skip = skip + 1
        elif new_folder_name != fol:
            prompt.warn("=====================")
            prompt.warn("Old : \t" + fol)
            prompt.warn("New : \t" + new_folder_name)

            if apply:
                os.rename(path, new_path)
                if os.path.exists(path) is False and os.path.exists(new_path):
                    change = change + 1
                else:
                    error = error + 1
        if apply or meta:
            utils.create_meta_file(folder, fol, new_folder_name)

    prompt.success(f"{change} element(s) changed")
    prompt.info(f"{skip} element(s) skipped")
    prompt.info(f"{remove} element(s) deleted")
    prompt.alert(f"{error} element(s) failed")
    prompt.line(f"{ignore} element(s) ignored")
    if len(delete_fail) > 0:
        prompt.line("The following folders couldn't be deleted")
        print(delete_fail)

    return
