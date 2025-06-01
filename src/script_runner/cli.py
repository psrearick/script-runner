from pathlib import Path
import sys
from typing import Any, Optional, Tuple

from script_runner.exceptions import AliasNotFoundError
from .runner import run_script
from .config import Registry
import click

@click.group()
def cli():
    """Script Runner - manage and run Python and shell scripts"""
    pass

@cli.command()
@click.argument('script_path', type=click.Path(exists=True, path_type=Path))
@click.option('--alias', '-a', type=str, help='Alias for the script.')
@click.option('--interpreter', '-i', type=click.Path(exists=True, path_type=Path),
              help='Specific interpreter to use (auto-detected if not specified)')
def add(script_path: Path, alias: Optional[str], interpreter: Optional[Path]):
    """Register a Python or shell script with an alias"""
    try:
        registry = Registry()
        registry.add_script(script_path, alias, interpreter)
        click.echo(f"Added script '{alias or script_path.stem}' -> {script_path}")
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
        script_type = script.get('type', 'python')
        click.echo(f"{script['alias']} ({script_type}): {script['path']}")

@cli.command()
def prune():
    """Remove all non-existent scripts and directories"""
    registry = Registry()
    for pruned in registry.prune():
        click.echo(f"Removed Alias: {pruned}")

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
