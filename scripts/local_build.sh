#!/bin/sh

pyenv update
pyenv install --list | grep 3.11

pyenv install 3.11.9

python -m pip install --upgrade pip
pip install --upgrade setuptools
pip install --upgrade virtualenv
pip install --upgrade poetry
pip install --upgrade poetry-dynamic-versioning
pip install --upgrade types-requests
pip install --upgrade types-PyYAML

poetry env use python
poetry env info

poetry dynamic-versioning enable

poetry lock
poetry update
poetry show --outdated
pip check

poetry lock
poetry update --lock
poetry install # --sync --without=dev

poetry run mypy musos_assist tests
poetry run flake8 #--output-file=build/flake8/flake8.txt
poetry run pytest --cov=musos_assist --cov-report=term-missing --cov-report=html:build/coverage-reports
poetry run behave

poetry run pdoc --output-dir docs musos_assist
# Update repo with final changes
poetry run cz bump --changelog --yes
poetry build

# poetry run twine check dist/*
