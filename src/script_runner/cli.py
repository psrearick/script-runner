import click

@click.group()
def cli():
    """Script Runner - manage and run Python scripts with virtual environments"""
    pass

@cli.command()
@click.argument('path')
@click.option('--alias', '-a', help='Alias for the script.')
@click.option('--venv-depth', 'd', help='Number of ancestors to search for virtual environment.')
@click.option('--venv', '-v', help='Path to virtual environment.')
@click.option('--no-venv', '-n', is_flag=True, help='Do not use a virtual environment.')
def add():
    """Add a script or directory to the registry"""
    click.echo('Add')

@cli.command()
@click.argument('script')
@click.argument('args', nargs=-1)
def run(script, args):
    """Run a registered script"""
    click.echo(f'Run {script} {args}')

@cli.command()
@click.argument('script')
@click.option('--alias', '-a', help='New alias for the directory or script.')
@click.option('--venv', '-v', help='Path to new virtual environment.')
@click.option('--no-venv', '-n', is_flag=True, help='Remove the virtual environment in the registry.')
def update():
    """Update a registered script or directory"""
    click.echo('Update')

@cli.command()
@click.argument('script')
def delete():
    """Delete a registered script or directory"""
    click.echo('Delete')

@cli.command()
def prune():
    """Remove all non-existent scripts and directories"""
    click.echo('Prune')

@cli.command()
@click.argument('directory')
def update_dir():
    """Register missing scripts in directory and prune it"""
    click.echo('Update Directory')

@cli.command()
def update_dirs():
    """Register missing scripts in all directories and prune them"""
    click.echo('Update Directories')
