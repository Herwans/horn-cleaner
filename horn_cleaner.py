import os
import click
import re
import json
import hashlib


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
    if os.path.exists("~/.horn/config.json") and os.path.isfile("~/.horn/config.json"):
        path = "~/.horn/config.json"
    elif os.path.exists("config.json") and os.path.isfile("config.json"):
        path = "config.json"

    if path is not None:
        with open(path, 'r') as f:
            data = json.load(f)
            return data["cli"]
    return None

def apply_folder_rules(element, rules):
    alteredElement = element
    for rule in rules:
        # 0 = Pattern
        # 1 = Replacement
        alteredElement = re.sub(rule[0], rule[1], alteredElement)
    alteredElement= alteredElement.strip()
    return alteredElement

def apply_file_rules(element, rules, sets):
    click.secho("File", fg="blue")
    alteredElement = element
    file_name, file_extension = os.path.splitext(element)
    alteredElement = file_name
    click.secho(element, fg="red")
    for rule in rules:
        if rule[2] == '*' or file_extension.lstrip(".") in sets[rule[2]]:
            click.secho(alteredElement, fg="red")
            alteredElement = alteredElement.strip()
            alteredElement = re.sub(rule[0], rule[1], alteredElement)
    alteredElement= alteredElement.strip()
    return alteredElement + file_extension

def create_meta_file(folder, currentName, newName):
    path = f"{folder}/{currentName}"
    if os.path.exists(path):
        if os.path.isfile(path):
            type = "file"
            metaPath = f"{folder}/{calculate_file_hash(path)}.json"
            if os.path.exists(metaPath):
                click.echo("Updating meta file...")
                with open(metaPath, 'r') as f:
                    metadata = json.load(f)
            else:
                click.echo("Creating meta file...")
                metadata = {}
                metadata["original_name"] = currentName
            metadata["new_name"] = newName
        elif os.path.isdir(path):
            type = "folder"
            metaPath = f"{folder}/{currentName}/meta.json"
            click.secho(metaPath)
            if os.path.exists(metaPath):
                click.echo("Updating meta file...")
                with open(metaPath, 'r') as f:
                    metadata = json.load(f)
            else:
                click.echo("Creating meta file...")
                metadata = {}
                metadata["original_name"] = currentName
            metadata["new_name"] = newName
        with open(metaPath, "w") as f:
            json.dump(metadata, f)
        click.secho("It's a " + type)


@click.command()
@click.option("--folder", default='.', help='This is the folder which the content will be cleaned')
@click.option("--apply", "-d", is_flag=True, default=False, help="When enable, apply modification")
def cli(folder, apply):
    """Allow to clean folder elements' name"""
    click.secho("===== ## HORN CLEANER ## ======", fg="blue")
    data = read_cli_config()
    if data is None:
        click.secho("No rules found", fg="red")
        return
    
    folderRules = data['folder-rules']
    fileRules = data['file-rules']
    sets = data['extension-set']
    originalElements = os.listdir(folder)

    change = 0
    skip = 0
    error = 0
    ignore = 0
    click.secho(f"{originalElements} in total")
    for element in originalElements:
        if os.path.splitext(element)[1] == ".json":
            ignore = ignore + 1
            continue

        click.secho("=====================", fg="blue")
        click.secho("Original : \t" + element, fg="yellow")
        alteredElement = element
        if os.path.isdir(f"./{folder}/{element}"): # If DIRECTORY
            alteredElement = apply_folder_rules(alteredElement, folderRules)
        elif os.path.isfile(f"./{folder}/{element}"): # IF FILE
            alteredElement = apply_file_rules(alteredElement, fileRules, sets)
        click.secho("New : \t\t" + alteredElement, fg="blue")
        if apply:
            create_meta_file(folder, element, alteredElement)
            if os.path.exists(f"{folder}/{alteredElement}") or alteredElement == element:
                skip = skip + 1
            else:
                os.rename(f"{folder}/{element}",f"{folder}/{alteredElement}")
                if os.path.exists(f"{folder}/{element}") == False and os.path.exists(f"{folder}/{alteredElement}"):
                    click.secho("New : " + alteredElement, fg="green")
                else:
                    error = error + 1
        
    click.secho(f"{change} element(s) changed", fg="green")
    click.secho(f"{skip} element(s) skipped", fg="blue")
    click.secho(f"{error} element(s) failed", fg="red")
    click.secho(f"{ignore} element(s) ignored", fg="white")

    return