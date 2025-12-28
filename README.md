# Template Project

This is a template repository setup with modern Python tooling:

- **Package Manager**: [uv](https://github.com/astral-sh/uv)
- **Linting & Formatting**: [Ruff](https://github.com/astral-sh/ruff)
- **Type Checking**: [mypy](https://mypy-lang.org/)
- **Testing**: [pytest](https://docs.pytest.org/)
- **Quality Checks**: [pre-commit](https://pre-commit.com/)

## Setup

1.  **Install uv**:
    ```sh
    # On macOS/Linux
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # On Windows
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

2.  **Install Dependencies**:
    ```sh
    uv sync
    ```

3.  **Setup Pre-commit** (Optional but recommended):
    ```sh
    # This installs the git hook to run checks before every commit
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
