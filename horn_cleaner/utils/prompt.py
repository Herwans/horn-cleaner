import click


def line(message):
    click.echo(message)


def info(message):
    click.secho(message, fg="blue")


def warn(message):
    click.secho(message, fg="yellow")


def success(message):
    click.secho(message, fg="green")


def alert(message):
    click.secho(message, fg="red")
