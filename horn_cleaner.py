import os
import click
import re
import json

def readCliConfig():
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

def applyFolderRules(element, rules):
    alteredElement = element
    for rule in rules:
        # 0 = Pattern
        # 1 = Replacement
        alteredElement = re.sub(rule[0], rule[1], alteredElement)
    alteredElement= alteredElement.strip()
    return alteredElement

def applyFileRules(element, rules, sets):
    click.secho("File", fg="blue")
    alteredElement = element
    file_name, file_extension = os.path.splitext(element)
    alteredElement = file_name
    click.secho(element, fg="red")
    for rule in rules:
        # Add a rule like "apply on everything"
        if rule[2] == '*' or file_extension.lstrip(".") in sets[rule[2]]:
            click.secho(alteredElement, fg="red")
            alteredElement = alteredElement.strip()
            alteredElement = re.sub(rule[0], rule[1], alteredElement)
    alteredElement= alteredElement.strip()
    return alteredElement + file_extension

def createMetaFile(folder, currentName, newName):
    path = f"{folder}/{currentName}"
    if os.path.exists(path):
        if os.path.isfile(path):
            type = "file"
        elif os.path.isdir(path):
            type = "folder"
            metaPath = f"{folder}/{currentName}/meta.json"
            click.secho(metaPath)
            if os.path.exists(metaPath):
                click.echo("Updating meta file...")
                with open(metaPath, 'r') as f:
                    metadata = json.load(f)
                    f.close()
                
            else:
                click.echo("Creating meta file...")
                metadata = {}
                metadata["original_name"] = currentName
            metadata["new_name"] = newName
            with open(metaPath, "w") as f:
                json.dump(metadata, f)
                f.close()
        click.secho("It's a " + type)


@click.command()
@click.option("--folder", default='.', help='This is the folder which the content will be cleaned')
@click.option("--apply", "-d", is_flag=True, default=False, help="When enable, apply modification")
def cli(folder, apply):
    """Allow to clean folder elements' name"""
    click.secho("===== ## HORN CLEANER ## ======", fg="blue")
    data = readCliConfig()
    if data is None:
        click.secho("No rules found", fg="red")
        return
    
    folderRules = data['folder-rules']
    fileRules = data['file-rules']
    sets = data['extension-set']
    originalElements = os.listdir(folder)

    for element in originalElements:
        click.secho("===================", fg="blue")
        click.secho("Original : " + element, fg="blue")
        alteredElement = element
        if os.path.isdir(f"./{folder}/{element}"): # If DIRECTORY
            alteredElement = applyFolderRules(alteredElement, folderRules)
        elif os.path.isfile(f"./{folder}/{element}"): # IF FILE
            alteredElement = applyFileRules(alteredElement, fileRules, sets)
        createMetaFile(folder, element, alteredElement)
        click.secho("New : " + alteredElement, fg="green")

    return
    print('Content of \'%s\' folder will be cleaned' % folder)
    longAssRegex = "(((\(([^)]+)\))|\s|(\[([^]]+)\])|(\{([^}]+)\}))*)"
    newElements = []


    for element in originalElements:
        alteredElement = element
        #alteredElement = re.sub("^\(C\d*\)","", alteredElement)
        #alteredElement = re.sub("\.torrent$","", alteredElement)
        #alteredElement = re.sub("\【(.*?)\】","", alteredElement)
        #alteredElement = re.sub("\「(.*?)\」","", alteredElement)
        #alteredElement = re.sub(f"{longAssRegex}$","", alteredElement)
        #alteredElement = re.sub(f"^{longAssRegex}","", alteredElement)
        alteredElement = alteredElement.strip()
        
        if alteredElement == "" or alteredElement in newElements:
            newElements.append(element)
        else:
            newElements.append(alteredElement)
    if apply == False:
        for i in range(len(originalElements)):
            click.secho(originalElements[i], fg='red')
            click.secho(newElements[i], fg='green')
            click.echo("========================")
    else:
        skip = 0
        for i in range(len(originalElements)):
            if originalElements[i] == newElements[i]: 
                skip+= 1
                continue
            click.secho(originalElements[i], fg='red')
            if os.path.exists(f"{folder}/{originalElements[i]}/meta.json"):
                click.echo("Meta file exists...")
            else:
                click.echo("Creating meta...")
                metadata = {}
                metadata["original_name"] = originalElements[i]
                metadata["new_name"] = newElements[i]
                with open(f"{folder}/{originalElements[i]}/meta.json", "w") as f:
                    json.dump(metadata, f)
            click.echo("Renaming...")
            if os.path.exists(f"{folder}/{newElements[i]}"):
                click.secho(f"Operation aborted, {newElements[i]} already present", fg='red')
                continue
            os.rename(f"{folder}/{originalElements[i]}",f"{folder}/{newElements[i]}")
            if os.path.exists(f"{folder}/{newElements[i]}"):
                click.secho(f"Folder successfully rename to {newElements[i]} already present", fg='green')
            click.echo("========================")
        click.secho(f"Skip: {skip}", fg='blue')

            
