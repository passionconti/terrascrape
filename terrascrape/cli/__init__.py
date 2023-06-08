import multiprocessing
import signal
import subprocess
import sys
from contextlib import suppress

import click

import terrascrape
from terrascrape.cli.run import run
from terrascrape.cli.utils.gunicorn_monitor import GunicornMonitor
from terrascrape.core.utils.update_components import update_whole_components

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

WELCOME_TITLE = r'''
  _______
 |__   __|
    | | ___ _ __ _ __ __ _ ___  ___ _ __ __ _ _ __   ___
    | |/ _ \ '__| '__/ _` / __|/ __| '__/ _` | '_ \ / _ \
    | |  __/ |  | | | (_| \__ \ (__| | | (_| | |_) |  __/
    |_|\___|_|  |_|  \__,_|___/\___|_|  \__,_| .__/ \___|
                                             | |
                                             |_|
'''


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """
        The Terrascrape CLI for build your own scrape pipeline.
    """
    pass


cli.add_command(run)


@cli.command(hidden=True)
def welcome():
    click.echo(WELCOME_TITLE)


@cli.command(hidden=True)
def config():
    click.echo(terrascrape.config.to_json())


@cli.command()
def webserver():
    """
    This command spins up all infrastructure and services for the Terrascrape server
    """
    num_workers = (multiprocessing.cpu_count() * 2) + 1
    run_args = [
        'gunicorn',
        '-w', str(num_workers),
        '-c', 'python:terrascrape.www.gunicorn_cfg',
        'terrascrape.www.run:app'
    ]
    gunicorn_master_proc = None

    def kill_proc(signum, _):
        gunicorn_master_proc.terminate()
        with suppress(TimeoutError):
            gunicorn_master_proc.wait(timeout=30)
        if gunicorn_master_proc.poll() is not None:
            gunicorn_master_proc.kill()
        sys.exit(0)

    def monitor_gunicorn(gunicorn_master_pid: int):
        signal.signal(signal.SIGINT, kill_proc)
        signal.signal(signal.SIGTERM, kill_proc)
        GunicornMonitor(gunicorn_master_pid=gunicorn_master_pid, num_workers_expected=num_workers).start()

    with subprocess.Popen(run_args, close_fds=True) as gunicorn_master_proc:
        monitor_gunicorn(gunicorn_master_proc.pid)


@cli.command()
def sync():
    """
        This command update all tasks in Task Directory
    """
    update_whole_components()


if __name__ == '__main__':
    cli()
