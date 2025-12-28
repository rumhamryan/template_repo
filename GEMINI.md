> A concise, agent-oriented guide to hacking on this project.
> Format reference: AGENTS.md open format.

SITUATION: You are an expert Python developer working with a modern Python project template.
CHALLENGE: Maintain strict code quality standards while initializing or extending projects based on this template.
AUDIENCE: Developers and Agents starting a new project or maintaining the template infrastructure.
FORMAT:
- Use clear, descriptive naming conventions.
- Adhere strictly to the configured linting rules (Ruff) and type checking (Mypy).
- Follow the principle of least surprise.
FOUNDATIONS:
- Prioritize static analysis and type safety.
- Use `uv` for all dependency management.
- Ensure `pre-commit` hooks pass before any commit.

## Project snapshot

- **Name**: template-project (configurable via setup script).
- **Python**: 3.12+.
- **Key Tooling**:
    - **uv**: Dependency management and virtual environments.
    - **Ruff**: Fast linting and formatting (replaces Black, Isort, Flake8).
    - **Mypy**: Strict static type checking.
    - **Pre-commit**: Git hooks for code quality.
- **Entrypoint**: `scripts/setup_project.py` (for initialization).

## Setup commands

To initialize a new project from this template:

```bash
# 1) Install uv (if not installed)
# pip install uv  --or--  curl -LsSf https://astral.sh/uv/install.sh | sh

# 2) Sync dependencies
uv sync

# 3) Install pre-commit hooks
uv run pre-commit install
```

## Run / Dev

The workflow depends on the project type initialized:

- **CLI**: Entrypoint at `src/<package>/__main__.py`.
- **Service**: Entrypoint at `src/<package>/app/main.py`.
- **Library**: API defined in `src/<package>/core/api.py`.

**Common commands:**

```bash
# Run the project (example for CLI)
uv run -m <package_name>

# Run a specific script
uv run scripts/some_script.py
```

## Tests

After fulfilling all prompt requests the following command must be run and return no errors:

```bash
# Run all tests
uv run pre-commit run --all-files
```

## Code style & tooling

- **Ruff**: Configured in `pyproject.toml`. Enforces `E`, `F`, `B`, `I`, `UP`, `SIM`, `PLR`.
    - Line length: 88.
    - Target version: Python 3.12.
- **Mypy**: configured for **strict** mode. `ignore_missing_imports = true`.
- **Pre-commit**: Runs `ruff format`, `ruff check`, and `mypy` (if configured) on staged files.

## Project structure

```text
├── .github/workflows/   # CI pipelines
├── scripts/             # Maintenance and setup scripts
│   └── setup_project.py # Project scaffolding tool
├── src/                 # Source code
├── src/
│   └── example_repo/
│       ├── app/
│       │   └── main.py      # Service entry point and wiring
│       ├── core/            # Domain logic (pure Python, no I/O)
│       ├── infra/           # External adapters (database, API clients)
│       └── __init__.py
├── tests/               # Test suite
│   ├── integration/     # Integration tests
│   └── unit/            # Unit tests
├── pyproject.toml       # Project configuration & dependencies
├── uv.lock              # Exact dependency versions
└── GEMINI.md            # Agent context (this file)
```

## Configuration

- **`pyproject.toml`**: The single source of truth for build, dependencies, and tool configuration.
- **`.pre-commit-config.yaml`**: Defines git hooks.

## Development Guidelines

1.  **Dependencies**: Always use `uv add <package>` or `uv add --dev <package>`. Do not edit `pyproject.toml` dependencies manually unless necessary.
2.  **Type Hints**: All new code **must** be fully typed. Mypy strict mode is enabled.
3.  **Linting**: Fix all linting errors. Use `uv run ruff check --fix .` for auto-fixes.
4.  **Tests (High Quality Bar)**:
    -   **Unit Tests** (`tests/unit`):
        -   **Coverage**: Every public function **must** have at least one test covering happy/error paths.
        -   **Isolation**: **Must** mock all I/O (network, disk, DB). No side effects.
    -   **Integration Tests** (`tests/integration`):
        -   **Purpose**: Verify components work together (e.g., CLI parsing -> Service -> DB).
        -   **Real I/O**: Allowed to use real file systems or local databases.
        -   **Scope**: Test full workflows or critical paths that unit tests cannot capture.
5.  **Secrets**: Never commit secrets. Use environment variables.

## What to do when adding features

1.  **Understand**: Read existing code to match style and patterns.
2.  **Test**: Create a test case that fails (TDD) or documents the new feature.
3.  **Implement**: Write the code, ensuring types are correct.
4.  **Verify**: Run `uv run pytest` and `uv run pre-commit run --all-files`.
