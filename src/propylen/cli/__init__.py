from propylen.functionality import *

import click

@click.group()
def cli():
    pass


@cli.command("init", help="Initialize a new project")
@click.argument("name", type=str, required=False)
@click.option("--interactive/--no-interactice", default=True)
@click.option("-n","--name", type=str, default=None, help="Name of the project")
@click.option("-p","--path", type=str, default=os.getcwd(), help="Path where the project will be created")
@click.option("-v","--version", type=str, default="0.1.0", help="The version of the project")
@click.option("--author", type=str, default="NOT_PROVIDED", help="The author of the project")
@click.option("--email", type=str, default="notprovided", help="The email of the author")
@click.option("--description", type=str, default="Some wild Python project", help="The description of the project")
@click.option("--license", "license_name", type=str, default="NA", help="The license of the project")
@click.option("--python-version", type=str, default="^3.6")
@click.option("--include-tests/--no-include-tests", default=True, help="Whether to include tests in the project")
@click.option("--executable/--no-executable", default=True, help="Whether to include __main__.py in the project")
def initialize_project_wrapper(name, path=os.getcwd(), version="0.1.0", author="NOT_PROVIDED", email="notprovided", description="Some wild Python project", license_name="NA", python_version="^3.6", include_tests=True, interactive=True, executable=True):
    initialize_project(name, path, version, author, email, description, license_name, python_version, include_tests, interactive, executable) 

       
        
@cli.command("reconcile", help="Reconcile Pipfile dependencies with 'pyproject.toml'")
def reconcile_dependencies_wrapper():
    deps = reconcile_dependencies()
    for package, version in deps.items():
        click.echo(f" - {package}: {version}")


@cli.command("install", help="Install packages")
@click.argument("packages", nargs=-1)
@click.option("-d", "--dev", is_flag=True, help="Install dev packages")
@click.option("--reconcile/--no-reconcile", default=True, is_flag=True, help="Reconcile dependencies")
def install_packages_wrapper(dev, packages, reconcile):
    install_packages(dev, packages, reconcile)

    
@cli.command("uninstall", help="Uninstall packages")
@click.argument("packages", nargs=-1)
@click.option("--reconcile/--no-reconcile", default=True, is_flag=True, help="Reconcile dependencies")
def uninstall_packages_wrapper(packages, reconcile):
    uninstall_packages(packages, reconcile)


@cli.command("build", help="Build a package into a wheel")
@click.option('--format', '-f', "build_format", type=click.Choice(['wheel', 'sdist', 'both']), default='both', help="Build format")
def build_wrapper(build_format):
    build(build_format)