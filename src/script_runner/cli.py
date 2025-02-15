from pathlib import Path
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
    click.echo(f'Add {path} {alias}')

@cli.command()
@click.argument('script', type=str)
@click.argument('args', nargs=-1)
def run(script: str, args):
    """Run a registered script"""
    click.echo(f'Run {script} {args}')

@cli.command()
@click.argument('name', type=str)
@click.option('--path', 'p', type=click.Path(exists=True, resolve_path=True), help='The new path to the registered script.')
@click.option('--alias', '-a', type=str, help='New alias for the directory or script.')
@click.option('--venv', '-v', type=click.Path(exists=True, resolve_path=True), help='Path to new virtual environment.')
@click.option('--no-venv', '-n', is_flag=True, show_default=True, default=False, help='Remove the virtual environment in the registry.')
def update(name: str, path: Path, alias: str, venv: Path, no_venv: bool):
    """Update a registered script or directory"""
    click.echo('Update')

@cli.command()
@click.argument('name', type=str)
def delete(name: str):
    """Delete a registered script or directory"""
    click.echo('Delete')

@cli.command()
def prune():
    """Remove all non-existent scripts and directories"""
    click.echo('Prune')

@cli.command()
@click.argument('directory', type=str)
def update_dir(directory: str):
    """Register missing scripts in directory and prune it"""
    click.echo('Update Directory')

@cli.command()
def update_dirs():
    """Register missing scripts in all directories and prune them"""
    click.echo('Update Directories')
