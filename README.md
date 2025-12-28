# Template Project

This is a template repository setup with modern Python tooling:

- **Package Manager**: [uv](https://github.com/astral-sh/uv)
- **Linting & Formatting**: [Ruff](https://github.com/astral-sh/ruff)
- **Type Checking**: [mypy](https://mypy-lang.org/)
- **Testing**: [pytest](https://docs.pytest.org/)
- **CI/Hooks**: [pre-commit](https://pre-commit.com/)

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

3.  **Setup Pre-commit**:
    ```sh
    # Activate virtual environment if not already
    # source .venv/bin/activate  # or .venv\Scripts\activate on Windows

    pre-commit install
    ```

## Development

- **Run Tests**: `uv run pytest`
- **Run Linter**: `uv run ruff check .`
- **Run Formatter**: `uv run ruff format .`
- **Type Check**: `uv run mypy .`
