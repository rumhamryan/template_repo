# Template Project

This is a template repository setup with modern Python tooling:

- **Package Manager**: [uv](https://github.com/astral-sh/uv)
- **Linting & Formatting**: [Ruff](https://github.com/astral-sh/ruff)
- **Type Checking**: [mypy](https://mypy-lang.org/)
- **Testing**: [pytest](https://docs.pytest.org/)

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

## Development Workflow

Before committing your code, run the following commands to ensure it meets quality standards. These checks are also run automatically in CI.

1.  **Lint & Format**:
    ```sh
    uv run ruff check . --fix
    uv run ruff format .
    ```

2.  **Type Check**:
    ```sh
    uv run mypy .
    ```

3.  **Run Tests**:
    ```sh
    uv run pytest
    ```

### One-liner for all checks
You can run all checks in sequence with this command:
```sh
uv run ruff check . --fix && uv run ruff format . && uv run mypy . && uv run pytest
```