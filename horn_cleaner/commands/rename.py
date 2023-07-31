import os
import click
from horn_cleaner.utils import utils


@click.command()
@click.argument("folder")
@click.option("--apply", "-a", is_flag=True, default=False, help="When enable, apply modification")
@click.option("--delete", "-d", is_flag=True, default=False, help="Delete empty folders")
@click.option("--meta", "-m", is_flag=True, default=False, help="Create meta file, include in apply")
def rename(folder, apply, delete, meta):
    """Allow to clean folder elements' name"""
    click.echo(f"{folder} folder content will be clean")
    config = utils.read_cli_config()
    if config is None:
        click.secho("No rules found", fg="red")
        return

    folder_rules = config['folder-rules']
    file_rules = config['file-rules']
    extension_sets = config['extension-set']

    original_elements = os.listdir(folder)
    click.secho(f"{len(original_elements)} elements have been found")

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

        click.secho("=====================", fg="blue")
        click.secho("Original : \t" + element, fg="yellow")
        altered_element = element
        if os.path.isdir(f"./{folder}/{element}"):  # If DIRECTORY
            if delete and utils.delete_folder(f"./{folder}/{element}"):
                remove = remove + 1
                continue
            else:
                altered_element = utils.apply_folder_rules(altered_element, folder_rules)
        elif os.path.isfile(f"./{folder}/{element}"):  # IF FILE
            altered_element = utils.apply_file_rules(altered_element, file_rules, extension_sets)

        click.secho("New : \t\t" + altered_element, fg="blue")

        if apply:
            utils.create_meta_file(folder, element, altered_element)
            if os.path.exists(f"{folder}/{altered_element}") or altered_element == element:
                skip = skip + 1
            else:
                os.rename(f"{folder}/{element}", f"{folder}/{altered_element}")
                if os.path.exists(f"{folder}/{element}") is False and os.path.exists(f"{folder}/{altered_element}"):
                    click.secho("New : " + altered_element, fg="green")
                    change = change + 1
                else:
                    error = error + 1
        elif meta:
            utils.create_meta_file(folder, element, altered_element)

    click.secho(f"{change} element(s) changed", fg="green")
    click.secho(f"{skip} element(s) skipped", fg="blue")
    click.secho(f"{remove} element(s) deleted", fg="blue")
    click.secho(f"{error} element(s) failed", fg="red")
    click.secho(f"{ignore} element(s) ignored", fg="white")
    if len(delete_fail) > 0:
        click.secho("The following folders couldn't be deleted")
        print(delete_fail)

    return


