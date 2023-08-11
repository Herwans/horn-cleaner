import os
import click
from horn_cleaner.utils import utils, prompt
from horn_cleaner.utils.path import Path


@click.command()
@click.argument("folder")
@click.option("--apply", "-a", is_flag=True, default=False, help="When enable, apply modification")
@click.option("--meta", "-m", is_flag=True, default=False, help="Create meta file, include in apply")
@click.option("--no-video-meta", "-n", is_flag=True, default=False, help="Prevent meta file creation for video")
@click.option("--delete", "-d", is_flag=True, default=False, help="Delete empty folders")
def rename(folder, apply, meta, no_video_meta, delete):
    """Allow to clean folder elements' name"""
    prompt.line(f"{folder} folder content will be clean")
    current = Path(folder)
    original_elements = current.children()
    prompt.line(f"{current.count()} elements have been found")

    change = 0
    skip = 0
    error = 0
    delete_fail = []
    ignore = 0
    remove = 0

    for element in original_elements:
        if os.path.splitext(element)[1] == ".json":
            ignore = ignore + 1
            continue

        prompt.info("=====================")
        prompt.warn("Original : \t" + element)
        altered_element = element
        if os.path.isdir(f"./{folder}/{element}"):  # If DIRECTORY
            if delete and utils.delete_folder(f"./{folder}/{element}"):
                remove = remove + 1
                continue
            else:
                altered_element = utils.apply_folder_rules(altered_element)
        elif os.path.isfile(f"./{folder}/{element}"):  # IF FILE
            altered_element = utils.apply_file_rules(altered_element)

        prompt.info("New : \t\t" + altered_element)

        if apply:
            if not (no_video_meta and utils.is_video(f"./{folder}/{element}")):
                utils.create_meta_file(folder, element, altered_element)
            if os.path.exists(f"{folder}/{altered_element}") or altered_element == element:
                skip = skip + 1
            else:
                os.rename(f"{folder}/{element}", f"{folder}/{altered_element}")
                if os.path.exists(f"{folder}/{element}") is False and os.path.exists(f"{folder}/{altered_element}"):
                    prompt.success("New : " + altered_element)
                    change = change + 1
                else:
                    error = error + 1
        elif meta and not (no_video_meta and utils.is_video(f"./{folder}/{element}")):
            utils.create_meta_file(folder, element, altered_element)

    prompt.success(f"{change} element(s) changed")
    prompt.info(f"{skip} element(s) skipped")
    prompt.info(f"{remove} element(s) deleted")
    prompt.alert(f"{error} element(s) failed")
    prompt.line(f"{ignore} element(s) ignored")
    if len(delete_fail) > 0:
        prompt.line("The following folders couldn't be deleted")
        print(delete_fail)

    return