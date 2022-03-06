import json
import os
import click
from click.exceptions import Exit
import toml
import pipenv
from  poetry.console.application import Application
from cleo import CommandTester

import emoji

poetry_version = "1.1.13"

def check_if_pyproject_toml_contains(path, name, path_keys):
    try:
        pyproject_toml_dict = toml.load("./pyproject.toml")
        
        element = pyproject_toml_dict
        for path_key in path_keys:
            element = element[path_key]
        return True, element
    except Exception:
        return False, None


def generate_new_pyproject_toml(name, path, version, author, email, description, license_name, python_version, include_tests):    
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
        pyproject_toml_dict["tool"]["pytest"] = {
                    "ini_options": {
                        "python_files": ["*test*.py"],
                        "python_functions": ["test"],
                        "minversion": "6.0",
                        "addopts": f"--cov={name} --cov-report=term-missing",
                        "testpaths": ["test"],
            }
        }
    
    with open(f"{path}/{name}/pyproject.toml", "w") as f:
        f.write(toml.dumps(pyproject_toml_dict))
        

def adjust_existing_pyproject_toml(name, path, version, author, email, description, license_name, python_version, interactive):
    existing_pyproject_toml_dict = toml.load(f"{path}/{name}/pyproject.toml")
            
    pyproject_toml_name = existing_pyproject_toml_dict.get("tool", {}).get("poetry", {}).get("name", None)
    if pyproject_toml_name is None and name is None:
        if interactive:
            name = click.prompt(emoji.emojize(":label: Project Name:"))
        else:
            click.echo(emoji.emojize(":warning: No name was found in pyproject.toml or provided in CLI. Please provide a name for a project."))
            
    pyproject_toml_version = existing_pyproject_toml_dict.get("tool", {}).get("poetry", {}).get("version", None)
    if pyproject_toml_version is None:
        if interactive:
            version = click.prompt(emoji.emojize(":input_numbers: Version:"), default=version)
                
    pyproject_toml_description = existing_pyproject_toml_dict.get("tool", {}).get("poetry", {}).get("description", None)
    if pyproject_toml_description is None:
        if interactive:
            pyproject_toml_description = click.prompt(emoji.emojize(":pen: Description:"), default=description)
            
    pyproject_toml_authors = existing_pyproject_toml_dict.get("tool", {}).get("poetry", {}).get("authors", None)
    if pyproject_toml_authors is None:
        if interactive:
            author = click.prompt(emoji.emojize(":nerd_face: Author:"), default='NOT_PROVIDED')
            email = click.prompt(emoji.emojize(":e-mail: Email:"), default='notprovided')
            
    pyproject_toml_license = existing_pyproject_toml_dict.get("tool", {}).get("poetry", {}).get("license", None)
    if pyproject_toml_license is None:
        if interactive:
            license_name = click.prompt(emoji.emojize(":scroll: License:"), default=license_name)
                    
    pyproject_toml_python_version = existing_pyproject_toml_dict.get("tool", {}).get("poetry", {}).get("dependencies", {}).get("python", None)
    if pyproject_toml_python_version is None:
        if interactive:
            python_version = click.prompt(emoji.emojize(":input_numbers: Python version:"), default=python_version)
            
    poetry_dict = {
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
                    }
            
    if 'tool' not in existing_pyproject_toml_dict:
        existing_pyproject_toml_dict['tool'] = {
                    "poetry": poetry_dict
                }
    elif 'poetry' not in existing_pyproject_toml_dict['tool']:
        existing_pyproject_toml_dict['tool']['poetry'] = poetry_dict
    else:
       existing_poetry_dict = existing_pyproject_toml_dict['tool']['poetry']
       existing_pyproject_toml_dict['tool']['poetry'] = {**poetry_dict, **existing_poetry_dict}
    with open(f"{path}/{name}/pyproject.toml", "w") as f:
        f.write(toml.dumps(existing_pyproject_toml_dict))
        

def generate_new_pipfile(name, path, include_tests):
    pipfile_dict = {
        "source" : [{
            "url": "https://pypi.org/simple",
            "verify_ssl": "true",
            "name": "pypi"
        }],
        "packages":{},
        "dev-packages":{"poetry": poetry_version},
        "scripts":{
            "build": "poetry build",
        }
    }
    
    if include_tests:
        pipfile_dict["dev-packages"]["pytest"] = "*"
        pipfile_dict["dev-packages"]["pytest-cov"] = "*"
        pipfile_dict["scripts"]["test"] = "pytest"
 
    with open(f"{path}/{name}/Pipfile", "w") as f:
        f.write(toml.dumps(pipfile_dict))
        
def adjust_existing_pipfile(name, path):
    existing_pipfile_dict = toml.load(f"{path}/{name}/Pipfile")
    if 'dev-packages' not in existing_pipfile_dict:
        existing_pipfile_dict['dev-packages'] = {"poetry": poetry_version}
    elif 'poetry' not in existing_pipfile_dict['dev-packages']:
        existing_pipfile_dict['dev-packages']['poetry'] = poetry_version
        
    with open(f"{path}/{name}/Pipfile", "w") as f:
        f.write(toml.dumps(existing_pipfile_dict))
         

def init_from_empty(path, version, author, email, description, license_name, python_version, include_tests, interactive, executable, name):
    click.echo(emoji.emojize(":sparkles: Initializing new awesome project...\n"))
    
    version, author, email, description, license_name, python_version, include_tests, executable, name = interactive_specifications(version, author, email, description, license_name, python_version, include_tests, interactive, executable, name)
    
    os.makedirs(f"{path}/{name}/src/{name}", exist_ok=True)
    with open(f"{path}/{name}/src/{name}/__init__.py", "w") as f:
        pass
    if executable:
        with open(f"{path}/{name}/src/{name}/__main__.py", "w") as f:
            pass
    
    if include_tests:
        os.makedirs(f"{path}/{name}/test/", exist_ok=True)

    generate_new_pyproject_toml(name, path, version, author, email, description, license_name, python_version, include_tests)
    generate_new_pipfile(name, path, include_tests)
        
    with open(f"{path}/{name}/README.md", "w") as f:
        f.write("# " + name + "\n")

    click.echo(emoji.emojize("\n:party_popper: You are all set, happy coding!"))

def interactive_specifications(version, author, email, description, license_name, python_version, include_tests, interactive, executable, name):
    if name is None:
        name = click.prompt(emoji.emojize(":label: Project Name:"))
    if interactive:
        version = click.prompt(emoji.emojize(":input_numbers: Version"), default=version)
        author = click.prompt(emoji.emojize(":nerd_face: Author"), default=author)
        email = click.prompt(emoji.emojize(":e-mail: Email:"), default=email)
        description = click.prompt(emoji.emojize(":pen: Description"), default=description)
        license_name = click.prompt(emoji.emojize(":scroll: License"), default=license_name)
        python_version = click.prompt(emoji.emojize(":input_numbers: Python version"), default=python_version)
        include_tests = click.confirm(emoji.emojize(":safety_vest: Include tests?"), default=include_tests)
        executable = click.confirm(emoji.emojize(":person_running: Include __main__.py?"), default=executable)
    return version,author,email,description,license_name,python_version,include_tests,executable,name


def initialize_project(name, path, version, author, email, description, license_name, python_version, include_tests, interactive, executable):
    path = path.rstrip("/")
    
    try:
        if name == None and any([i in os.listdir(path) for i in ["Pipfile", "pyproject.toml", "src", "test"]]):
            click.echo(emoji.emojize(":warning: Detected project directory, not creating a new one."))
            split_path = path.split("/")
            name = split_path[-1]
            path = '/'.join(split_path[:-1])
        directory_content = os.listdir(f"{path}/{name}")
    except Exception:
        directory_content = []
    if any([i in directory_content for i in ["Pipfile", "pyproject.toml", "src", "test", "README"]]):
        click.echo(emoji.emojize(":warning: Project already exists."))
        os.makedirs(f"{path}/{name}/src/{name}", exist_ok=True)
        os.makedirs(f"{path}/{name}/test", exist_ok=True)
        if 'Pipfile' not in directory_content:
            if name is None:
                name = click.prompt(emoji.emojize(":label: Project Name"))
            click.echo(emoji.emojize(":warning: 'Pipfile' not found, creating one..."))
            generate_new_pipfile(name, path, include_tests)
        else:
            click.echo(emoji.emojize(":warning: 'Pipfile' found, adjusting for propylen..."))
            adjust_existing_pipfile(name, path)

        if 'pyproject.toml' not in directory_content:
            version, author, email, description, license_name, python_version, include_tests, executable, name = interactive_specifications(version, author, email, description, license_name, python_version, include_tests, interactive, executable, name)
            click.echo(emoji.emojize(":warning: 'pyproject.toml' not found, creating one..."))
            generate_new_pyproject_toml(name, path, version, author, email, description, license_name, python_version, include_tests)
        else:
            click.echo(emoji.emojize(":warning: 'pyproject.toml' found, adjusting for propylen..."))
            adjust_existing_pyproject_toml(name, path, version, author, email, description, license_name, python_version, interactive)
    else:
        init_from_empty(path, version, author, email, description, license_name, python_version, include_tests, interactive, executable, name)  


def reconcile_dependencies():
    click.echo(emoji.emojize(':mag: Reconciling dependencies...'))
    
    dir_content = os.listdir("./")
    if 'Pipfile' not in dir_content or 'pyproject.toml' not in dir_content:
        click.echo(emoji.emojize(":warning: 'Pipfile' or 'pyproject.toml' not found. Run `propylen init` first."))
        exit(1)
    
    pipfile_dict = toml.load("./Pipfile")
    
    pyproject_toml_dict = toml.load("./pyproject.toml")
    
    proactive_versioning = pyproject_toml_dict.get("tool", {}).get("propylen", {}).get("proactive_versioning", True)
    try:
        
        python_version = pyproject_toml_dict["tool"]["poetry"]["dependencies"]["python"]
        packages = pipfile_dict["packages"]
    
    except KeyError:
        
        click.echo(emoji.emojize(":warning: pyproject.toml or Pipfile doesn't contain expected fields, did you run `propylen init`?"))
        exit(1)
        
    try:
        
        with open("./Pipfile.lock", "r") as f:
            lock_dict = json.load(f)
        
        packages = {k: lock_dict['default'][k]['version'].replace("==", "^") if (v == '*' and proactive_versioning) else v for k, v in packages.items()}
    
    except KeyError:
        
        click.echo(emoji.emojize(":package: No Pipfile.lock found, installing packages"))
        install_packages(False, [])
        with open("./Pipfile.lock", "r") as f:
            lock_dict = json.load(f)
        
        packages = {k: lock_dict['default'][k]['version'].replace("==", "^") if (v == '*' and proactive_versioning) else v for k, v in packages.items()}
        
    packages_version = packages.copy()
    
    packages["python"] = python_version
    
    pyproject_toml_dict["tool"]["poetry"]["dependencies"] = packages
    

    with open("./pyproject.toml", "w") as f:
        f.write(toml.dumps(pyproject_toml_dict))
        
    return packages_version

def install_packages(dev, packages, reconcile):
    dir_content = os.listdir("./")
    if 'Pipfile' not in dir_content or 'pyproject.toml' not in dir_content:
        click.echo(emoji.emojize(":warning: 'Pipfile' or 'pyproject.toml' not found. Run `propylen init` first."))
        exit(1)
    if len(packages) != 0:
        click.echo(emoji.emojize(f":plus: Installing packages: {packages}"))
    else:
        click.echo(emoji.emojize(":package: Installing packages"))
    command = ['install']
    if dev:
        command.append("--dev")
    command.extend(packages)
    try:
        pipenv.cli.main(command)
    except Exception:
        pass
    finally:
        if reconcile or toml.load("./pyproject.toml")["tool"].get("propylen", {}).get("auto_reconcile_dependencies", False):
            reconcile_dependencies()
            
            
def uninstall_packages(packages, reconcile):
    dir_content = os.listdir("./")
    if 'Pipfile' not in dir_content or 'pyproject.toml' not in dir_content:
        click.echo(emoji.emojize(":warning: 'Pipfile' or 'pyproject.toml' not found. Run `propylen init` first."))
        exit(1)
    click.echo(emoji.emojize(f":minus: Uninstalling packages: {packages}"))
    command = ['uninstall']
    command.extend(packages)
    try:
        pipenv.cli.main(command)
    except Exception:
        pass
    finally:
        if reconcile or toml.load("./pyproject.toml")["tool"].get("propylen", {}).get("auto_reconcile_dependencies", False):
            reconcile_dependencies()


def build(build_format):
    click.echo(emoji.emojize(":building_construction: Building"))
    application = Application()
    reconcile_dependencies()
    
    command = application.find("build")
    run = CommandTester(command)
    run.execute(f"--format {build_format}" if not build_format=="both" else "")

