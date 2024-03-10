import os
import click
from vulcan.utils import utils, prompt
from vulcan.utils.path import Path


def print_difference(old_value, new_value):
    prompt.info("=====================")
    prompt.info("Old : \t" + old_value)
    prompt.info("New : \t" + new_value)


@click.command()
@click.argument("folder")
@click.option("--dry-run", "-d", "dryrun", is_flag=True, default=False, help="Prevent modification")
@click.option("--delete", is_flag=True, default=False, help="Delete empty folders")
@click.option("--verbose", "-v", is_flag=True, default=False, help="Show information alongside the execution")
def rename(folder, dryrun, delete, verbose):
    """Allow to clean folder elements' name"""
    if verbose:
        prompt.line(f"{folder} folder content will be clean")
    parent_folder = Path(folder)
    if verbose:
        prompt.line(f"{parent_folder.count()} elements have been found")

    change = 0
    skip = 0
    error = 0
    delete_fail = []
    ignore = 0
    remove = 0
    dr_new_files_names = []
    dr_new_folders_names = []

    for current_file in parent_folder.files(True):
        new_file_name = utils.apply_file_rules(current_file)

        full_file_path = os.path.join(folder, current_file)
        new_full_file_path = os.path.join(folder, new_file_name)

        # Check if the new file name doesn't already exist
        if os.path.exists(new_full_file_path):
            skip += 1
        elif new_file_name != current_file:
            if dryrun:
                # Check if another file already plan this name
                if new_full_file_path not in dr_new_files_names:
                    print_difference(full_file_path, new_full_file_path)
                    dr_new_files_names.append(new_full_file_path)
                    change += 1
                else:
                    prompt.info(f"File ignore: {current_file}")
                    skip += 1
            else:
                if verbose:
                    print_difference(full_file_path, new_full_file_path)
                os.rename(full_file_path, new_full_file_path)
                if os.path.exists(full_file_path) is False and os.path.exists(new_full_file_path):
                    change += 1
                else:
                    error += 1

    for current_folder in parent_folder.folders(True):
        if dryrun is False and delete and utils.delete_folder(current_folder):
            remove += 1
            continue

        new_folder_name = utils.apply_folder_rules(current_folder)
        full_file_path = os.path.join(folder, current_folder)
        new_full_file_path = os.path.join(folder, new_folder_name)

        if os.path.exists(new_full_file_path):
            skip = skip + 1
        elif new_folder_name != current_folder:
            if dryrun:
                # Check if another folder already plan this name
                if new_full_file_path not in dr_new_folders_names:
                    print_difference(full_file_path, new_full_file_path)
                    dr_new_folders_names.append(new_full_file_path)
                    change += 1
                else:
                    skip += 1
            else:
                if verbose:
                    print_difference(full_file_path, new_full_file_path)

                os.rename(full_file_path, new_full_file_path)
                if os.path.exists(full_file_path) is False and os.path.exists(new_full_file_path):
                    change = change + 1
                else:
                    error = error + 1

    if dryrun:
        prompt.success(f"{change} element(s) will change")
        prompt.info(f"{skip} element(s) will be skipped")
        prompt.info(f"{remove} element(s) will be deleted")
        prompt.line(f"{ignore} element(s) will be ignored")
    elif verbose:
        prompt.success(f"{change} element(s) changed")
        prompt.info(f"{skip} element(s) skipped")
        prompt.info(f"{remove} element(s) deleted")
        prompt.alert(f"{error} element(s) failed")
        prompt.line(f"{ignore} element(s) ignored")
    if len(delete_fail) > 0:
        if verbose:
            prompt.line("The following folders couldn't be deleted")
        print(delete_fail)

    return
