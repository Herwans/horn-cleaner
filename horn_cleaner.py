import os
import click
import re
import json

@click.command()
@click.option("--folder", default='.', help='This is the folder which the content will be cleaned')
# @click.option("--settings", default=nil, help='Define the behavior of the command')
@click.option("--dryrun", "-d", is_flag=True, default=True, help="When enable, prevent modification and just show the potential result")
def cli(folder, dryrun):
    """Allow to clean folder elements' name"""
    print('Content of \'%s\' folder will be cleaned' % folder)
    longAssRegex = "(((\(([^)]+)\))|\s|(\[([^]]+)\])|(\{([^}]+)\}))*)"
    originalElements = os.listdir(folder)
    newElements = []


    for element in originalElements:
        alteredElement = element
        alteredElement = re.sub("^\(C\d*\)","", alteredElement)
        alteredElement = re.sub("\.torrent$","", alteredElement)
        alteredElement = re.sub("\【(.*?)\】","", alteredElement)
        alteredElement = re.sub("\「(.*?)\」","", alteredElement)
        alteredElement = re.sub(f"{longAssRegex}$","", alteredElement)
        alteredElement = re.sub(f"^{longAssRegex}","", alteredElement)
        alteredElement= alteredElement.strip()
        
        if alteredElement == "" or alteredElement in newElements:
            newElements.append(element)
        else:
            newElements.append(alteredElement)
    if dryrun:
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

            
