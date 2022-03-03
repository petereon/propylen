import os
import click
import toml
import pipenv
from  poetry.console.application import Application
from cleo import CommandTester

from rich.console import Console
from rich.theme import Theme
custom_theme = Theme({
    "info": "dim cyan",
    "comment": "italic magenta",
    "danger": "bold red"
})

console = Console(theme=custom_theme)


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
    if interactive:
        version = click.prompt("Version:", default=version)
        author = click.prompt("Author:", default=author)
        email = click.prompt("Email:", default=email)
        description = click.prompt("Description:", default=description)
        license_name = click.prompt("License:", default=license_name)
        python_version = click.prompt("Python version:", default=python_version)
        include_tests = click.confirm("Include tests?", default=include_tests)
        executable = click.confirm("Include __main__.py?", default=executable)
        
    
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
        
        
    
    with open(f"{path}/{name}/Pipfile", "w") as f:
        f.write(toml.dumps(pipfile_dict))
    
    with open(f"{path}/{name}/pyproject.toml", "w") as f:
        f.write(toml.dumps(pyproject_toml_dict))
        
    with open(f"{path}/{name}/README", "w") as f:
        f.write("# " + name + "\n")
    
@cli.command("reconcile", help="Reconcile Pipfile dependencies with pyproject.toml")
def reconcile_dependencies():
    pipfile_dict = toml.load(f"./Pipfile")
    pyproject_toml_dict = toml.load(f"./pyproject.toml")
    
    python_version = pyproject_toml_dict["tool"]["poetry"]["dependencies"]["python"]
    packages = pipfile_dict["packages"]
    packages = {k: v.replace("==", "") for k, v in packages.items()}
    
    packages["python"] = python_version
    
    pyproject_toml_dict["tool"]["poetry"]["dependencies"] = packages
    

    with open(f"./pyproject.toml", "w") as f:
        f.write(toml.dumps(pyproject_toml_dict))
        
@cli.command("install", help="Install packages")
@click.option("-d", "--dev", is_flag=True, help="Install dev packages")
@click.argument("packages", nargs=-1)
def install_packages(dev, packages):
    command = ['install']
    if dev:
        command.append("--dev")
    command.extend(packages)
    print(pipenv.cli.main(command))
    
    
@cli.command("uninstall", help="Uninstall packages")
@click.argument("packages", nargs=-1)
def install_packages(packages):
    command = ['uninstall']
    command.extend(packages)
    print(pipenv.cli.main(command))


@cli.command("build", help="Build a package into a wheel")
@click.option('--format', '-f', "build_format", type=click.Choice(['wheel', 'sdist', 'both']), default='both', help="Build format")
def install_packages(build_format):
    application = Application()
    
    command = application.find("build")
    run = CommandTester(command)
    
    run.execute(f"--format {build_format}" if not build_format=="both" else "")