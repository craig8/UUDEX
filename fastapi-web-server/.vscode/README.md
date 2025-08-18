# VS Code Configuration for UUDEX FastAPI Server

This directory contains VS Code configuration for automatic linting, formatting, and development.

## Setup

1. Install the recommended extensions when prompted by VS Code, or manually install:
   - Python (ms-python.python)
   - Ruff (charliermarsh.ruff) 
   - MyPy Type Checker (ms-python.mypy-type-checker)

2. The project will automatically use the virtual environment in `.venv/`

3. Linting and formatting will happen automatically on save

## Available Tasks

Press `Ctrl+Shift+P` and type "Tasks: Run Task" to access:

- **ruff-check**: Run ruff linter
- **ruff-fix**: Run ruff linter with auto-fix
- **ruff-format**: Run ruff formatter
- **mypy-check**: Run mypy type checking  
- **lint-all**: Run all linting tools (default build task)
- **test**: Run tests with pytest

Or use `Ctrl+Shift+P` → "Tasks: Run Build Task" to run the default linting task.

## Linting Configuration

- **Ruff**: Fast Python linter and formatter (configured in `pyproject.toml`)
  - Line length: 100 characters
  - Includes import sorting, code modernization, and error detection
  
- **MyPy**: Static type checking (configured in `pyproject.toml`)
  - Checks type annotations and catches type errors
  
- **Pre-commit hooks**: Automatically run linting on git commits
  - Installed with `poetry run pre-commit install`

## Manual Commands

```bash
# Run linting
poetry run ruff check src/ tests/ --fix
poetry run ruff format src/ tests/
poetry run mypy src/

# Run all linting
poetry run pre-commit run --all-files

# Run tests
poetry run pytest tests/ -v
```

## Configuration Files

- `.vscode/settings.json`: VS Code Python and linting settings
- `.vscode/extensions.json`: Recommended extensions
- `.vscode/tasks.json`: Build and test tasks
- `pyproject.toml`: Ruff and MyPy configuration
- `.pre-commit-config.yaml`: Git pre-commit hooks