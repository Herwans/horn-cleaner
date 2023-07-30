import os
import click
import re
import json
import hashlib
import pathlib


def calculate_file_hash(file_path, hash_algorithm='sha256'):
    try:
        with open(file_path, 'rb') as f:
            hasher = hashlib.new(hash_algorithm)
            while chunk := f.read(8192):
                hasher.update(chunk)
            return hasher.hexdigest()
    except FileNotFoundError:
        return None


def read_cli_config():
    path = None
    default_path = f"{pathlib.Path.home()}/.horn/config.json"
    if os.path.exists(default_path) and os.path.isfile(default_path):
        path = default_path
    elif os.path.exists("config.json") and os.path.isfile("config.json"):
        path = "config.json"

    if path is not None:
        with open(path, 'r') as f:
            data = json.load(f)
            return data["cli"]
    return None


def apply_folder_rules(element, rules):
    altered_element = element
    for rule in rules:
        # 0 = Pattern
        # 1 = Replacement
        altered_element = re.sub(rule[0], rule[1], altered_element)
    altered_element = altered_element.strip()
    return altered_element


def apply_file_rules(element, rules, sets):
    file_name, file_extension = os.path.splitext(element)
    altered_element = file_name
    for rule in rules:
        if len(rule) == 4:
            exclusion = rule[3].split(',')
        else:
            exclusion = []
        if (rule[2] == '*' or file_extension.lstrip(".") in sets[rule[2]])\
                and file_extension.lstrip(".") not in exclusion:
            altered_element = altered_element.strip()
            altered_element = re.sub(rule[0], rule[1], altered_element)
    altered_element = altered_element.strip()
    return altered_element + file_extension


def create_meta_file(folder, current_name, new_name):
    global metadata_path, element_type
    path = f"{folder}/{current_name}"
    if os.path.exists(path):
        if os.path.isfile(path):
            element_type = "file"
            metadata_path = f"{folder}/{calculate_file_hash(path)}.json"
            if os.path.exists(metadata_path):
                click.echo("Updating meta file...")
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
            else:
                click.echo("Creating meta file...")
                metadata = {"original_name": current_name}
            metadata["new_name"] = new_name
        elif os.path.isdir(path):
            element_type = "folder"
            metadata_path = f"{folder}/{current_name}/meta.json"
            click.secho(metadata_path)
            if os.path.exists(metadata_path):
                click.echo("Updating meta file...")
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
            else:
                click.echo("Creating meta file...")
                metadata = {"original_name": current_name}
            metadata["new_name"] = new_name
        with open(metadata_path, "w") as f:
            json.dump(metadata, f)
        click.secho("It's a " + element_type)


def delete_folder(path):
    elements = os.listdir(path)
    to_delete = pathlib.Path(path)
    if len(elements) == 0:
        pathlib.Path.rmdir(to_delete)
        return True
    elif len(elements) == 1 and elements[0] == "meta.json":
        os.remove(path + "/meta.json")
        pathlib.Path.rmdir(to_delete)
        return True
    return False


@click.command()
@click.option("--folder", default='.', help='This is the folder which the content will be cleaned')
@click.option("--apply", "-a", is_flag=True, default=False, help="When enable, apply modification")
@click.option("--delete", "-d", is_flag=True, default=False, help="Delete empty folders")
@click.option("--meta", "-m", is_flag=True, default=False, help="Create meta file, include in apply")
def cli(folder, apply, delete, meta):
    """Allow to clean folder elements' name"""
    click.secho("===== ## HORN CLEANER ## ======", fg="blue")
    data = read_cli_config()
    if data is None:
        click.secho("No rules found", fg="red")
        return

    folder_rules = data['folder-rules']
    file_rules = data['file-rules']
    sets = data['extension-set']
    original_elements = os.listdir(folder)

    change = 0
    skip = 0
    error = 0
    delete_fail = []
    ignore = 0
    remove = 0
    click.secho(f"{len(original_elements)} in total")
    for element in original_elements:
        if os.path.splitext(element)[1] == ".json":
            ignore = ignore + 1
            continue

        click.secho("=====================", fg="blue")
        click.secho("Original : \t" + element, fg="yellow")
        altered_element = element
        if os.path.isdir(f"./{folder}/{element}"):  # If DIRECTORY
            if delete and delete_folder(f"./{folder}/{element}"):
                remove = remove + 1
                continue
            else:
                altered_element = apply_folder_rules(altered_element, folder_rules)
        elif os.path.isfile(f"./{folder}/{element}"):  # IF FILE
            altered_element = apply_file_rules(altered_element, file_rules, sets)

        click.secho("New : \t\t" + altered_element, fg="blue")

        if apply:
            create_meta_file(folder, element, altered_element)
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
            create_meta_file(folder, element, altered_element)

    click.secho(f"{change} element(s) changed", fg="green")
    click.secho(f"{skip} element(s) skipped", fg="blue")
    click.secho(f"{remove} element(s) deleted", fg="blue")
    click.secho(f"{error} element(s) failed", fg="red")
    click.secho(f"{ignore} element(s) ignored", fg="white")
    if len(delete_fail) > 0:
        click.secho("The following folders couldn't be deleted")
        print(delete_fail)

    return
