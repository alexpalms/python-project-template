# text-to-fight


### Code quality

#### Package structure

- Scheme:
```
text-to-fight/
├── pyproject.toml
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

