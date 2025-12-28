# Template Project

This is a template repository setup with modern Python tooling:

- **Package Manager**: [uv](https://github.com/astral-sh/uv)
- **Linting & Formatting**: [Ruff](https://github.com/astral-sh/ruff)
- **Type Checking**: [mypy](https://mypy-lang.org/)
- **Testing**: [pytest](https://docs.pytest.org/)
- **Quality Checks Local**: [pre-commit](https://pre-commit.com/)
- **Quality Checks Remote**: [Github Action](https://docs.github.com/en/actions)

## Getting Started

### 1. Prerequisite: Install uv
The project uses `uv` for fast dependency management. It is a required dependency.
```sh
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Initialize Your Project
Run the automated setup script. This will:
- Rename the project in `pyproject.toml`.
- Create your package directory structure.
- Remove template placeholder files.
- **Automatically install pre-commit git hooks.**

```sh
# Clone the repo, then run:
uv run scripts/setup_project.py --name my_project_name --type cli

# Available types: library, cli, service
```

## Development Workflow

### Mandatory Quality Checks
This project enforces quality standards via `pre-commit`.

To run all checks manually (recommended before pushing):
```sh
uv run pre-commit run --all-files
```

### Individual Tools
- **Test**: `uv run pytest`
- **Lint**: `uv run ruff check .`
- **Format**: `uv run ruff format .`
- **Type Check**: `uv run mypy .`
