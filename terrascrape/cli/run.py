import click


@click.group()
def run():
    """
    Run some component of Terrascrape
    \b
    Usage:
        $ terrascrape run [COMMAND]
    """
    pass


@run.command(name="terra")
@click.argument("name")
def run_terra(name):
    """
    Run specific terra only
    \b
    Arguments:
        Name         TEXT    Name of terra
    """
    try:
        # todo run specific terra
        click.echo(f"Run {name} terra successfully.")
    except Exception:
        # todo handle error
        pass
