# Propylen

__Propylen__ is a Python CLI tool for generating Python projects. In nature, it is a wrapper around pipenv and poetry with some added swag.

# Installation

__Propylen__ should be installed using `pipx` as:
```
pipx install propylen
```

# Usage

## Initialize project

You can generate a project structure interactively:
```
propylen init <project-name>
```

Alternatively, you can provide necessary infromation in form of command line options. To see available options:
```
propylen -h
```
## Package Management

__pipenv__ is used as a backend for package management. Options are stripped down.

You can also use `propylen` to install packages using
```
propylen install <package-name1> <package-name2> ...
```
Or without package name to install dependencies from `Pipfile`
```
propylen install
```

Additional options are also available, to see them:
```
propylen install -h
```

You can uninstall packages using
```
propylen uninstall <package-name1> <package-name2> ...
```

## Building

__poetry__ is used as a backend for building. Options are stripped down.

You can build the project using
```
propylen build
```

Additional options are also available, to see them:
```
propylen build -h
```