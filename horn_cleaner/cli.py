import click
from horn_cleaner.commands.rename import rename


@click.group()
def cli():
    click.secho("===== ## HORN CLEANER ## ======", fg="blue")
    pass


cli.add_command(rename)

if __name__ == "__main__":
    cli()
