from typing import Tuple
from functools import lru_cache

import tomli as tomllib


@lru_cache()
def get_app_info() -> Tuple[str, str, str]:
    """
    get app info from pyproject.toml
    :return: a tuple with application name, author, version
    """
    with open("pyproject.toml", "rb") as py_project_file:
        py_project_data = tomllib.load(py_project_file)
    project = py_project_data["project"]
    _name = project["name"]
    _authors = project["authors"]
    _author = _authors[0]["name"]
    _version = project["version"]
    return _name, _author, _version


application_name, author, version = get_app_info()
