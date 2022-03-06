# Propylen

__Propylen__ is a Python CLI tool for generating Python projects. In nature, it is a wrapper around pipenv and poetry with some added swag.

__NOTE: Package is not yet fully tested__

# Installation

__Propylen__ should be installed using `pipx` as:
```shell
pipx install propylen
```

# Usage

## Initialize project

Propylen generates project structure of type:
```
{project-name} 
 |- src/
     |- {project-name}
         |- __init__.py
         |- __main__.py
 |- test/
 |- Pipfile
 |- pyproject.toml
 |- README.md
```

You can generate a project structure interactively:
```shell
propylen init <project-name>
```

Alternatively, you can provide necessary infromation in form of command line options. To see available options:
```shell
propylen init -h
```
## Package Management

`pipenv` is used as a backend for package management. Options are stripped down.

Propylen reconciles packages installed using `pipenv` (to `Pipfile`) to the `pyproject.toml` file. This behavior can be disabled temporarily by calling `propylen install` or `propylen uninstall` with `--no-reconcile` option or permanently by adding `auto_reconcile_dependencies = false` into `[tool.propylen]` section of `pyproject.toml`

By default propylen tries to proactively version packages in `pyproject.toml` if no version is provided in `Pipfile`. This behavior can be disabled by adding `proactive_versioning = false` into `[tool.propylen]` section of `pyproject.toml`.

You can also use `propylen` to install packages using
```shell
propylen install <package-name1> <package-name2> ...
```
Or without package name to install dependencies from `Pipfile`
```shell
propylen install
```

Additional options are also available, to see them:
```shell
propylen install -h
```

You can uninstall packages using
```shell
propylen uninstall <package-name1> <package-name2> ...
```

You can reconcile packages from `Pipfile` to `pyproject.toml` using
```shell
propylen reconcile
```
Unless it is unset as described above it happens automatically during installs and uninstalls.

## Building

__poetry__ is used as a backend for building. Options are stripped down.

You can build the project using
```shell
propylen build
```

Additional options are also available, to see them:
```shell
propylen build -h
```