from pathlib import Path
import sys
from typing import Any, Optional, Tuple

from script_runner.exceptions import AliasNotFoundError
from .runner import run_script
from .config import Registry
import click

@click.group()
def cli():
    """Script Runner - manage and run Python scripts with virtual environments"""
    pass

@cli.command()
@click.argument('script_path', type=click.Path(exists=True, path_type=Path))
@click.option('--alias', '-a', type=str, help='Alias for the script.')
@click.option('--python', '-p', type=click.Path(exists=True, path_type=Path),
              help='Python executable to use (auto-detected if not specified)')
def add(path: Path, alias: Optional[str], python: Optional[Path]):
    """Register a Python script with an alias"""
    try:
        registry = Registry()
        registry.add_script(path, alias, python)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

@cli.command()
def list():
    """List registered scripts"""
    registry = Registry()
    if not registry.scripts:
        click.echo("No scripts registered")
        return

    for script in registry.scripts:
        click.echo(f"{script['alias']}: {script['path']}")

@cli.command()
def prune():
    """Remove all non-existent scripts and directories"""
    registry = Registry()
    registry.prune()

@cli.command()
@click.argument('alias', type=str)
def remove(alias: str):
    """Delete a registered alias"""
    try:
        registry = Registry()
        registry.remove_alias(alias)
    except AliasNotFoundError as e:
        click.echo(e, err=True)
    except:
        click.echo('Failed to Delete Item')

@cli.command()
@click.argument('alias', type=str)
@click.argument('args', nargs=-1)
def run(alias: str, args: Tuple[Any] = tuple()):
    """Run a registered script"""
    try:
        registry = Registry()
        script = registry.get_script(alias)
        if not script:
            click.echo(f"Error: Alias '{alias}' not found", err=True)
            sys.exit(1)

        run_script(script, args)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
