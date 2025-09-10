# text-to-fight


### Badges

<a href="https://arxiv.org/abs/2508.00641"><img src="https://img.shields.io/badge/paper-arXiv:2508.00641-B31B1B?logo=arxiv" alt="Paper"/></a>
<a href="https://alexpalms.github.io/"><img src="https://img.shields.io/badge/Blog-Read%20Post-blue" alt="Blog Post"/></a>
<a href="https://artificialtwin.com/"><img src="https://img.shields.io/badge/Project-View%20Page-gold" alt="Company Project"/></a>

<a href="https://github.com/alexpalms/text-to-fight/actions/workflows/code-formatting-check.yaml"><img src="https://github.com/alexpalms/text-to-fight/actions/workflows/code-formatting-check.yaml?label=code%20formatting&logo=github" alt="Code Formatting"/></a>
<a href="https://github.com/diambra/arena/actions/workflows/test_agents.yaml"><img src="https://img.shields.io/github/actions/workflow/status/diambra/arena/test_agents.yaml?label=agents%20tests&logo=github" alt="Agents Test"/></a>

<a href="https://github.com/diambra/arena/tags"><img src="https://img.shields.io/github/v/tag/diambra/arena?label=latest%20tag&logo=github" alt="Latest Tag"/></a>
<a href="https://pypi.org/project/diambra-arena/"><img src="https://img.shields.io/pypi/v/diambra-arena?logo=pypi" alt="Pypi version"/></a>

<a href="https://github.com/alexpalms/text-to-fight"><img src="https://img.shields.io/badge/supported%20os-linux%20%7C%20win%20%7C%20macOS-blue?logo=docker" alt="Supported OS"/></a>

<a href="https://github.com/alexpalms/text-to-fight"><img src="https://img.shields.io/github/last-commit/alexpalms/text-to-fight/main?label=repo%20latest%20update&logo=readthedocs" alt="Latest Repo Update"/></a>


[![codecov](https://codecov.io/github/alexpalms/text-to-fight/graph/badge.svg?token=4817P3HFDN)](https://codecov.io/github/alexpalms/text-to-fight)


![Ruff](https://img.shields.io/badge/linting-ruff-4B8BBE?logo=python&logoColor=white)
![mypy](https://img.shields.io/badge/type%20checking-mypy-2A6DB0.svg)

![Python Versions](https://img.shields.io/pypi/pyversions/diambra-arena)
![Python >=3.9](https://img.shields.io/badge/python-%3E%3D3.9-blue)

![Docker Pulls](https://img.shields.io/docker/pulls/diambra/engine)
![PyPI Downloads](https://img.shields.io/pypi/dm/diambra-arena)
![Docker Image Version](https://img.shields.io/docker/v/diambra/engine?sort=semver)


![License](https://img.shields.io/github/license/alexpalms/text-to-fight)


### Code quality



#### Package structure

- Scheme:
```
text-to-fight/
├── pyproject.toml
├── docker/
│   └── Dockerfile
│   └── entrypoint.sh
├── examples/
│   └── example_1.py
├── src/
│   └── text_to_fight/
│       ├── __init__.py
│       ├── llm_chat.py
│       └── agents.py
├── scripts/
│   └── diambra_run.py
├── tests/
│   └── __init__.py
├── requirements.txt   # optional, for legacy pip users

```

- Install `uv` ([Ref](https://github.com/astral-sh/uv))
  - `pip install uv` in the general python environment (not inside virtual envs)
  - Add `export PATH="$HOME/.local/bin:$PATH"` to `~/.bashrc`

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
      - `uv add pyright`
      - Configurations for `pyright` in `root/pyrightconfig.json`
      - Run it locally from the root with `uv run pyright`
    - `mypy`
      - `uv add mypy`
      - Configurations for `mypy` in `root/pyprojects.toml`
      - Run it locally from the root with `uv run mypy`
  - Pre-commit
    - `uv add pre-commit`
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
    - `uv add ruff`
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
    - `uv add pytest pytest-cov`
    - Configurations for `pytest` in `.vscode/settings.json`
    - Run it locally from the root with:
      - `uv run pytest`
      - `uv run pytest --cov=text_to_fight --cov-report=term-missing --cov-report=xml`
  - CI/CD
    - See `root/.github/workflows/pytest.yaml`
