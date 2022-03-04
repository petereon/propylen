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

You can generate a project structure interactively:
```shell
propylen init <project-name>
```

Alternatively, you can provide necessary infromation in form of command line options. To see available options:
```shell
propylen init -h
```
## Package Management

__pipenv__ is used as a backend for package management. Options are stripped down.

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