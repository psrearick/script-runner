from pathlib import Path
from .runner import run_script
from .config import Registry
import click

@click.group()
def cli():
    """Script Runner - manage and run Python scripts with virtual environments"""
    pass

@cli.command()
@click.argument('path', type=click.Path(exists=True, resolve_path=True))
@click.option('--alias', '-a', type=str, help='Alias for the script.')
@click.option('--venv-depth', '-d', type=int, default=3, show_default=True, help='Number of ancestors to search for virtual environment.')
@click.option('--venv', '-v', type=click.Path(exists=True, resolve_path=True), help='Path to virtual environment.')
@click.option('--no-venv', '-n', is_flag=True, show_default=True, default=False, help='Do not use a virtual environment.')
def add(path: Path, alias: str, venv_depth: int, venv: Path, no_venv: bool):
    """Add a script or directory to the registry"""
    registry = Registry()
    if no_venv:
        venv = False
    registry.add_script(path, alias=alias, venv=venv, venv_depth=venv_depth)

@cli.command()
@click.argument('script', type=str)
@click.argument('args', nargs=-1)
def run(script: str, args):
    """Run a registered script"""
    registry = Registry()
    script_info = registry.get_script(script)
    if script_info:
        run_script(script_info, args)
    else:
        click.echo(f"Script '{script}' not found")

@cli.command()
@click.argument('name', type=str)
@click.option('--path', 'p', type=click.Path(exists=True, resolve_path=True), help='The new path to the registered script.')
@click.option('--alias', '-a', type=str, help='New alias for the directory or script.')
@click.option('--venv', '-v', type=click.Path(exists=True, resolve_path=True), help='Path to new virtual environment.')
@click.option('--no-venv', '-n', is_flag=True, show_default=True, default=False, help='Remove the virtual environment in the registry.')
def update(name: str, path: Path, alias: str, venv: Path, no_venv: bool):
    """Update a registered script or directory"""
    registry = Registry()
    try:
        registry.update_script(name, path, alias, venv, no_venv)
    except:
        click.echo('Failed to Update Registry')

@cli.command()
@click.argument('name', type=str)
def delete(name: str):
    """Delete a registered script or directory"""
    registry = Registry()
    try:
        registry.delete_script(name)
    except:
        click.echo('Failed to Delete Item')

@cli.command()
def prune():
    """Remove all non-existent scripts and directories"""
    registry = Registry()
    registry.prune()

@cli.command()
@click.argument('directory', type=str)
def update_dir(directory: str):
    """Register missing scripts in directory and prune it"""
    registry = Registry()
    try:
        registry.update_directory(directory)
    except:
        click.echo('Failed to Update Directory')

@cli.command()
def update_dirs():
    """Register missing scripts in all directories and prune them"""
    registry = Registry()
    registry.update_directories()
