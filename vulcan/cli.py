import click

from vulcan.commands.garbage import garbage
from vulcan.commands.integrity import integrity
from vulcan.commands.rename import rename


@click.group()
def cli():
    pass


cli.add_command(rename)
cli.add_command(integrity)
cli.add_command(garbage)

if __name__ == "__main__":
    cli()
