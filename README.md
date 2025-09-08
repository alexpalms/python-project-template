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
  - `.vscode/settings.json`
    ```json
    {
    "editor.parameterHints.enabled": true,          // inline hint suggestions
    "editor.inlayHints.enabled": "on",               // show inferred types in editor
    }
    ```
  - `root/pyrightconfig.json`
    ```
    {
    "python.analysis.typeCheckingMode": "strict",   // enforce strict typing
    "typeCheckingMode": "strict",
    "reportMissingParameterType": "warning",
    "reportMissingTypeArgument": "warning",
    "reportUntypedFunctionDecorator": "warning",
    "reportUntypedFunctionCall": "warning",
    "reportMissingTypeStubs": "none"
    }
    ```
- Extra
  - Local check
    - Pip package for `mypy`
    - Configurations for `mypy` in pyprojects.toml
      ```toml
      [tool.mypy]
      strict = true
      python_version = "3.11"
      files = ["src", "scripts"]#, "tests"]
      ```
    - Run it locally from the root with `mypy`
  - Pre-commit
    - Pip package `pre-commit`
    - Define pre-commit configuration file `.pre-commit-config.yaml`:
      ```yaml
      repos:
        - repo: https://github.com/pre-commit/mirrors-mypy
          rev: v1.17.1
          hooks:
            - id: mypy
              language: system
              entry: mypy
              args: ["--strict"]
              additional_dependencies: []  # example: type stubs
      ```
    - Install pre-commit hook `pre-commit install`
    - Run it locally ``

