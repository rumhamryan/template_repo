# Template Project

This is a template repository setup with modern Python tooling:

- **Package Manager**: [uv](https://github.com/astral-sh/uv)
- **Linting & Formatting**: [Ruff](https://github.com/astral-sh/ruff)
- **Type Checking**: [mypy](https://mypy-lang.org/)
- **Testing**: [pytest](https://docs.pytest.org/)
- **Quality Checks**: [pre-commit](https://pre-commit.com/)

## Getting Started

1.  **Clone the repository** (or use "Use this template").

2.  **Initialize your project**:
    Run the setup script to rename the project and create the directory structure.
    ```sh
    # Example: Create a CLI app named 'my_cool_tool'
    python scripts/setup_project.py --name my_cool_tool --type cli

    # Available types: library, cli, service
    ```

3.  **Install uv**:
    ```sh
    # On macOS/Linux
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # On Windows
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

4.  **Install Dependencies**:
    ```sh
    uv sync
    ```

5.  **Setup Pre-commit** (Required):
    This installs the git hook to run checks before every commit.
    ```sh
    uv run pre-commit install
    ```

## Development Workflow

### Running Checks Manually

You can use `pre-commit` to run all quality checks (linting, formatting, types, tests) at once. This ensures your code is ready for CI.

```sh
uv run pre-commit run --all-files
```

### Individual Tools

If you need to run tools individually during debugging:

- **Test**: `uv run pytest`
- **Lint**: `uv run ruff check .`
- **Format**: `uv run ruff format .`
- **Type Check**: `uv run mypy .`
