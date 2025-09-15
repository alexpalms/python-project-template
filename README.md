# Python Project Template

This repository serves as a template for Python projects, designed to streamline setup and reduce boilerplate. It provides a ready-to-use structure with best practices for packaging, dependency management, documentation, and continuous deployment. By starting from this template, you can focus on building your code and features instead of spending time on repetitive project setup tasks.

### Badges

<a href="https://arxiv.org/abs/2508.00641"><img src="https://img.shields.io/badge/paper-arXiv:2508.00641-B31B1B?logo=arxiv" alt="Paper"/></a>
<a href="https://alexpalms.github.io/"><img src="https://img.shields.io/badge/blog-read%20post-blue" alt="Blog Post"/></a>
<a href="https://artificialtwin.com/"><img src="https://img.shields.io/badge/project-view%20page-gold" alt="Company Project"/></a>

<a href="https://github.com/diambra/arena/actions/workflows/type-hints-check.yaml"><img src="https://img.shields.io/github/actions/workflow/status/alexpalms/python-project-template/type-hints-check.yaml?label=type%20hints&logo=github" alt="Type Hints"/></a>
<a href="https://github.com/diambra/arena/actions/workflows/code-formatting-check.yaml"><img src="https://img.shields.io/github/actions/workflow/status/alexpalms/python-project-template/code-formatting-check.yaml?label=code%20formatting&logo=github" alt="Code Formatting"/></a>
<a href="https://github.com/diambra/arena/actions/workflows/pytest.yaml"><img src="https://img.shields.io/github/actions/workflow/status/alexpalms/python-project-template/pytest.yaml?label=pytest&logo=github" alt="Pytest"/></a>


<a href="https://github.com/diambra/arena/tags"><img src="https://img.shields.io/github/v/tag/diambra/arena?label=latest%20tag&logo=github" alt="Latest Tag"/></a>

<a href="https://pypi.org/project/diambra-arena/"><img src="https://img.shields.io/pypi/v/diambra-arena?logo=pypi" alt="Pypi version"/></a>
![PyPI Downloads](https://img.shields.io/pypi/dm/diambra-arena)

<a href="https://github.com/alexpalms/python-project-template"><img src="https://img.shields.io/badge/supported%20os-linux%20%7C%20win%20%7C%20macOS-blue?logo=docker" alt="Supported OS"/></a>

<a href="https://github.com/alexpalms/python-project-template"><img src="https://img.shields.io/github/last-commit/alexpalms/python-project-template/main?label=repo%20latest%20update&logo=readthedocs" alt="Latest Repo Update"/></a>
<a href="https://github.com/alexpalms/python-project-template"><img src="https://img.shields.io/github/last-commit/alexpalms/python-project-template/main?label=docs%20latest%20update&logo=readthedocs" alt="Latest Docs Update"/></a>


[![codecov](https://codecov.io/github/alexpalms/python-project-template/graph/badge.svg?token=4817P3HFDN)](https://codecov.io/github/alexpalms/python-project-template)


![Ruff](https://img.shields.io/badge/linting-ruff-4B8BBE?logo=python&logoColor=white)
![mypy](https://img.shields.io/badge/type%20checking-mypy-2A6DB0?logo=python&logoColor=white)
![pytest](https://img.shields.io/badge/testing-pytest-2A6DB0?logo=python&logoColor=white)

![Python Versions](https://img.shields.io/pypi/pyversions/diambra-arena)
![Python >=3.9](https://img.shields.io/badge/python-%3E%3D3.9-blue)

![Docker Image Version](https://img.shields.io/docker/v/diambra/engine?sort=semver)
![Docker Pulls](https://img.shields.io/docker/pulls/diambra/engine)

![License](https://img.shields.io/github/license/alexpalms/python-project-template?cacheBust=1)

### Dev environment setup

- Install `uv` ([Ref](https://github.com/astral-sh/uv))
  - `pip install uv` in the general python environment (not inside virtual envs)
  - Add `export PATH="$HOME/.local/bin:$PATH"` to `~/.bashrc`
- Install package with dependencies `uv pip install -e .`
- Install package with group dependencies `uv pip install -e . --group dev`

### Code quality

#### Package structure

- Scheme:
```
python-project-template/
├── pyproject.toml
├── pyrightconfig.json
├── codecov.json
├── .github/
│   └── ISSUE_TEMPLATE/
│       └── bug_report.md
│       └── config.yaml
│       └── feature_request.md
│   └── PULL_REQUEST_TEMPLATE.md
│   └── workflows/
│       └── code-formatting-check.yaml
│       └── pytest.yaml
│       └── type-hints-check.yaml
├── .vscode/
│   └── launch.json
│   └── settings.json
│   └── tasks.json
├── .pre-commit-config.yaml
├── LICENSE
├── .gitignore
├── docker/
│   └── Dockerfile
│   └── entrypoint.sh
├── docs/
│   └── build/
│   └── source/
│       └── _static/
│           └── favicon.ico
│       └── _templates/
│       └── conf.py
│       └── index.rst
│   └── Makefile
├── examples/
│   └── example_1.py
├── src/
│   └── project_name/
│       ├── __init__.py
│       └── agents.py
│       └── utils.py
│       └── cli.py
├── tests/
│   └── test_agents.py
├── requirements.txt   # optional, for legacy pip users

```

#### Type Hints

- Extensions:
  - Python / Pylance (`ms-python.vscode-pylance`)
  - mypy
- Settings:
  See settings under
  - `.vscode/settings.json`
  - `root/pyrightconfig.json`
- Extra
  - Local check
    - `pyright`
      - `uv add --group dev pyright`
      - Configurations for `pyright` in `root/pyrightconfig.json`
      - Run it locally from the root with `uv run pyright`
    - `mypy`
      - `uv add --group dev mypy`
      - Configurations for `mypy` in `root/pyprojects.toml`
      - Run it locally from the root with `uv run mypy`
  - Pre-commit
    - `uv add --group dev pre-commit`
    - Define pre-commit configuration file `root/.pre-commit-config.yaml`
    - Install pre-commit hook `uv run pre-commit install`
    - Run it locally `uv run pre-commit run --all-files`
  - CI/CD
    - See `root/.github/workflows/type-hints-check.yaml`

#### Code Formatting

- Extensions:
  - Ruff
- Settings:
  See settings under
  - `.vscode/settings.json`
  - `root/pyproject.toml`
- Extra
  - Local check
    - `uv add --group dev ruff`
    - Configurations for `ruff` in `root/pyproject.toml`
    - Run it locally from the root with:
      - `uv run ruff check . ` for checking
      - `uv run ruff format --check . ` for format
  - Pre-commit
    - `uv add pre-commit`
    - Define pre-commit configuration file `root/.pre-commit-config.yaml`
    - Install pre-commit hook `uv run pre-commit install`
    - Run it locally `uv run pre-commit run --all-files`
  - CI/CD
    - See `root/.github/workflows/code-formatting-check.yaml`

#### Testing

- Extensions:
  - Python
- Settings:
  See settings under
  - `.vscode/settings.json`
- Extra
  - Local check
    - `uv add --group dev pytest pytest-cov`
    - Configurations for `pytest` in `.vscode/settings.json`
    - Run it locally from the root with:
      - `uv run pytest`
      - `uv run pytest --cov=text_to_fight --cov-report=term-missing --cov-report=xml`
  - CI/CD
    - See `root/.github/workflows/pytest.yaml`
    - Code coverage:
      - Managed via: https://app.codecov.io/
      - Settings in `codecov.yaml` and docs available at https://docs.codecov.com/docs/common-recipe-list

### Docs

- `uv add --group docs sphinx furo sphinx-autodoc-typehints myst-parser sphinx-autobuild`
- from the repo root `uv run sphinx-quickstart docs`
- from the repo root `uv run sphinx-apidoc -o docs/source/ src/project_name --separate`
- For building:
  - With autobuild: from repo root run `uv run sphinx-autobuild docs/source docs/build/html`
  - Manually: from inside `docs` run `uv run make html`


### Packaging

- Build package with `uv build`
- Check package locally using twine:
  - Install with `uv add --group dev twine`
  - Run it with `uv run twine check dist/*`
- Test locally from build wheel: `uv pip install dist/project_name-0.1.0-py3-none-any.whl`
- Push to Pypi registry:
  - Test:
    - `uv publish --repository testpypi`
    - `uv pip install --index-url https://test.pypi.org/simple/ my-package`
  - Official: `uv publish`