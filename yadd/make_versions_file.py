from ismain import is_main

from pathlib import Path


import tomli as tomllib


def make_versions_file():

    """
    get app info from pyproject.toml and write to __version__.py
    """
    with open("pyproject.toml", "rb") as py_project_file:
        py_project_data = tomllib.load(py_project_file)
    project = py_project_data["project"]
    _name = project["name"]
    _authors = project["authors"]
    _author = _authors[0]["name"]
    _version = project["version"]

    with Path("yadd", "__version__.py").open("w") as f:
        f.write(f'application_name = "{_name}"\n')
        f.write(f'author = "{_author}"\n')
        f.write(f'version = "{_version}"\n')


if is_main():
    make_versions_file()