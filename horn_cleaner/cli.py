import click

from horn_cleaner.commands.garbage import garbage
from horn_cleaner.commands.integrity import integrity
from horn_cleaner.commands.rename import rename
from horn_cleaner.commands.simplify import simplify


@click.group()
def cli():
    pass


cli.add_command(rename)
cli.add_command(integrity)
cli.add_command(garbage)
cli.add_command(simplify)

if __name__ == "__main__":
    cli()
