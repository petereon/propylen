import json
import os
import click
from click.exceptions import Exit
import toml
import pipenv
from  poetry.console.application import Application
from cleo import CommandTester

import emoji


@click.group()
def cli():
    pass


@cli.command("init", help="Initialize a new project")
@click.argument("name", type=str, required=False)
@click.option("--interactive/--no-interactice", default=True)
@click.option("-n","--name", type=str, prompt="Project name", help="Project name")
@click.option("-p","--path", type=str, default=os.getcwd(), help="Path where the project will be created")
@click.option("-v","--version", type=str, default="0.1.0", help="The version of the project")
@click.option("--author", type=str, default="NOT_PROVIDED", help="The author of the project")
@click.option("--email", type=str, default="notprovided", help="The email of the author")
@click.option("--description", type=str, default="Some wild Python project", help="The description of the project")
@click.option("--license", "license_name", type=str, default="NA", help="The license of the project")
@click.option("--python-version", type=str, default="^3.6")
@click.option("--include-tests/--no-include-tests", default=True, help="Whether to include tests in the project")
@click.option("--executable/--no-executable", default=True, help="Whether to include __main__.py in the project")
def initialize_project(name, path=os.getcwd(), version="0.1.0", author="NOT_PROVIDED", email="notprovided", description="Some wild Python project", license_name="NA", python_version="^3.6", include_tests=True, interactive=True, executable=True):
    click.echo(emoji.emojize(":sparkles: Initializing new awesome project...\n"))
    
    if interactive:
        version = click.prompt(emoji.emojize(":input_numbers: Version:"), default=version)
        author = click.prompt(emoji.emojize(":nerd_face: Author:"), default=author)
        email = click.prompt(emoji.emojize(":e-mail: Email:"), default=email)
        description = click.prompt(emoji.emojize(":pen: Description:"), default=description)
        license_name = click.prompt(emoji.emojize(":scroll: License:"), default=license_name)
        python_version = click.prompt(emoji.emojize(":input_numbers: Python version:"), default=python_version)
        include_tests = click.confirm(emoji.emojize(":safety_vest: Include tests?"), default=include_tests)
        executable = click.confirm(emoji.emojize(":person_running: Include __main__.py?"), default=executable)
    
    os.makedirs(f"{path}/{name}/src/{name}", exist_ok=True)
    with open(f"{path}/{name}/src/{name}/__init__.py", "w") as f:
        pass
    if executable:
        with open(f"{path}/{name}/src/{name}/__main__.py", "w") as f:
            pass
    
    pipfile_dict = {
        "source" : [{
            "url": "https://pypi.org/simple",
            "verify_ssl": "true",
            "name": "pypi"
        }],

        "packages":{},
        
        "dev-packages":{"poetry": "*"},

        "scripts":{
            "build": "poetry build",
        }
    }
    
    pyproject_toml_dict = {
        "tool": {
            "poetry": {
                "name": name,
                "version": version,
                "description": description,
                "authors": [f"{author} <{email}>"],
                "license": license_name,
                "dependencies": {
                    "python": python_version
                },
                "packages": [
                    {"include": name, "from": "src"}
                ]
            },
            
        },
        "build-system": {
            "requires": ["poetry-core>=1.0.0"],
            "build-backend": "poetry.core.masonry.api"
        }
    }
    
    if include_tests:
        os.makedirs(f"{path}/{name}/test", exist_ok=True)
        
        pipfile_dict["dev-packages"]["pytest"] = "*"
        pipfile_dict["dev-packages"]["pytest-cov"] = "*"
        pipfile_dict["scripts"]["test"] = "pytest"
        
        pyproject_toml_dict["tool"]["pytest"] = {
                    "ini_options": {
                        "python_files": ["*test*.py"],
                        "python_functions": ["test"],
                        "minversion": "6.0",
                        "addopts": f"--cov={name} --cov-report=term-missing",
                        "testpaths": ["test"],
            }
        }
    click.echo(emoji.emojize("\n:party_popper: You are all set, happy coding!"))
        
        
    
    with open(f"{path}/{name}/Pipfile", "w") as f:
        f.write(toml.dumps(pipfile_dict))
    
    with open(f"{path}/{name}/pyproject.toml", "w") as f:
        f.write(toml.dumps(pyproject_toml_dict))
        
    with open(f"{path}/{name}/README.md", "w") as f:
        f.write("# " + name + "\n")
        
        


def reconcile_dependencies():
    click.echo(emoji.emojize(':mag: Reconciling dependencies...'))
    pipfile_dict = toml.load("./Pipfile")
    pyproject_toml_dict = toml.load("./pyproject.toml")
    
    proactive_versioning = pyproject_toml_dict["tool"]["propylen"]["proactive_versioning"]
    
    python_version = pyproject_toml_dict["tool"]["poetry"]["dependencies"]["python"]
    
    packages = pipfile_dict["packages"]
    
    with open("./Pipfile.lock", "r") as f:
        lock_dict = json.load(f)
    try:
        packages = {k: lock_dict['default'][k]['version'].replace("==", "^") if (v == '*' and proactive_versioning) else v for k, v in packages.items()}
    except KeyError:
        install_packages(False, [])
        
    packages_version = packages.copy()
    
    packages["python"] = python_version
    
    pyproject_toml_dict["tool"]["poetry"]["dependencies"] = packages
    

    with open("./pyproject.toml", "w") as f:
        f.write(toml.dumps(pyproject_toml_dict))
        
    return packages_version
    
        
        
@cli.command("reconcile", help="Reconcile Pipfile dependencies with pyproject.toml")
def reconcile_dependencies_wrapper():
    deps = reconcile_dependencies()
    for package, version in deps.items():
        click.echo(f" - {package}: {version}")


def install_packages(dev, packages, reconcile):
    command = ['install']
    if dev:
        command.append("--dev")
    command.extend(packages)
    try:
        pipenv.cli.main(command)
    except Exception:
        pass
    finally:
        if reconcile or toml.load("./pyproject.toml")["tool"]["propylen"]["auto_reconcile_dependencies"]:
            reconcile_dependencies()

        
@cli.command("install", help="Install packages")
@click.argument("packages", nargs=-1)
@click.option("-d", "--dev", is_flag=True, help="Install dev packages")
@click.option("--reconcile/--no-reconcile", default=True, is_flag=True, help="Reconcile dependencies")
def install_packages_wrapper(dev, packages, reconcile):
    if len(packages) != 0:
        click.echo(emoji.emojize(f":plus: Installing packages: {packages}"))
    else:
        click.echo(emoji.emojize(":package: Installing packages"))
    install_packages(dev, packages, reconcile)

    
@cli.command("uninstall", help="Uninstall packages")
@click.argument("packages", nargs=-1)
@click.option("--reconcile/--no-reconcile", default=True, is_flag=True, help="Reconcile dependencies")
def uninstall_packages(packages, reconcile):
    click.echo(emoji.emojize(f":minus: Uninstalling packages: {packages}"))
    command = ['uninstall']
    command.extend(packages)
    try:
        pipenv.cli.main(command)
    except Exception:
        pass
    finally:
        if reconcile or toml.load("./pyproject.toml")["tool"]["propylen"]["auto_reconcile_dependencies"]:
            reconcile_dependencies()


@cli.command("build", help="Build a package into a wheel")
@click.option('--format', '-f', "build_format", type=click.Choice(['wheel', 'sdist', 'both']), default='both', help="Build format")
def build(build_format):
    click.echo(emoji.emojize(":building_construction: Building"))
    application = Application()
    reconcile_dependencies()
    
    command = application.find("build")
    run = CommandTester(command)
    run.execute(f"--format {build_format}" if not build_format=="both" else "")