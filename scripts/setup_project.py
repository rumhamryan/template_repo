#!/usr/bin/env python3
"""
Initialize a Python project directory structure based on project type.

Supported project types:
  - library
  - cli
  - service

Features:
  - Canonical src/<package> layout
  - Mirrored tests/<package> layout
  - Optional --dry-run mode
  - Safe: refuses to overwrite existing files

Examples:
  python scripts/init_project.py --name my_lib --type library
  python scripts/init_project.py --name my_cli --type cli
  python scripts/init_project.py --name my_service --type service --dry-run
"""

from __future__ import annotations

import argparse
import sys
import shutil
import re
from pathlib import Path


PROJECT_TYPES = {"library", "cli", "service"}


def die(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def log(action: str, path: Path, dry_run: bool) -> None:
    prefix = "[DRY-RUN]" if dry_run else "[CREATE]"
    print(f"{prefix} {action}: {path}")


def touch_init(path: Path, *, dry_run: bool) -> None:
    if path.exists():
        return

    log("dir", path, dry_run)
    log("file", path / "__init__.py", dry_run)

    if not dry_run:
        path.mkdir(parents=True, exist_ok=True)
        (path / "__init__.py").touch(exist_ok=True)


def create_file(path: Path, content: str, *, dry_run: bool) -> None:
    if path.exists():
        die(f"Refusing to overwrite existing file: {path}")

    log("file", path, dry_run)

    if not dry_run:
        path.write_text(content, encoding="utf-8")


def update_pyproject_name(new_name: str, *, dry_run: bool) -> None:
    pyproject_path = Path.cwd() / "pyproject.toml"
    if not pyproject_path.exists():
        print(f"warning: {pyproject_path} not found, skipping name update.")
        return

    log("update", pyproject_path, dry_run)
    if dry_run:
        return

    content = pyproject_path.read_text(encoding="utf-8")
    # Robust regex to replace name = "..." or name='...'
    # Assumes 'name' is in the [project] table or top level.
    # It catches `name = "template-project"`
    new_content = re.sub(
        r'^(name\s*=\s*)(["\']).*?(["\'])',
        f'\\1\\2{new_name}\\3',
        content,
        flags=re.MULTILINE
    )
    
    if content == new_content:
        print("  (no changes made to pyproject.toml name)")
    else:
        pyproject_path.write_text(new_content, encoding="utf-8")


def cleanup_legacy(root: Path, *, dry_run: bool) -> None:
    """Removes the initial template placeholders."""
    legacy_src = root / "src" / "template_project"
    legacy_test = root / "tests" / "test_basic.py"

    if legacy_src.exists():
        prefix = "[DRY-RUN] [DELETE]" if dry_run else "[DELETE]"
        print(f"{prefix} {legacy_src}")
        if not dry_run:
            shutil.rmtree(legacy_src)

    if legacy_test.exists():
        prefix = "[DRY-RUN] [DELETE]" if dry_run else "[DELETE]"
        print(f"{prefix} {legacy_test}")
        if not dry_run:
            legacy_test.unlink()


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize project structure.")
    parser.add_argument(
        "--name",
        required=True,
        help="Python package name (used under src/ and tests/)",
    )
    parser.add_argument(
        "--type",
        required=True,
        choices=sorted(PROJECT_TYPES),
        help="Project type",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be created without touching the filesystem",
    )

    args = parser.parse_args()
    package_name = args.name
    project_type = args.type
    dry_run = args.dry_run

    root = Path.cwd()
    src_pkg = root / "src" / package_name
    tests_root = root / "tests"
    tests_pkg = tests_root / package_name

    if src_pkg.exists():
        die(f"Target package directory already exists: {src_pkg}")

    if not package_name.isidentifier():
        die(
            f"--name must be a valid Python identifier (use underscores, not hyphens). "
            f"Example: plex_o_tron (not plex-o-tron). Got: {package_name!r}"
        )

    # ------------------------------------------------------------------
    # Update Configuration
    # ------------------------------------------------------------------
    # Convert package_name (snake_case) to kebab-case for the project name in toml
    project_name = package_name.replace("_", "-")
    update_pyproject_name(project_name, dry_run=dry_run)

    # ------------------------------------------------------------------
    # src/<package> layout
    # ------------------------------------------------------------------
    touch_init(src_pkg, dry_run=dry_run)
    touch_init(src_pkg / "core", dry_run=dry_run)

    if project_type in {"cli", "service"}:
        touch_init(src_pkg / "app", dry_run=dry_run)

    if project_type == "service":
        touch_init(src_pkg / "infra", dry_run=dry_run)

    # Type-specific source files
    if project_type == "library":
        create_file(
            src_pkg / "core" / "api.py",
            "# Public library API\n",
            dry_run=dry_run,
        )

    if project_type == "cli":
        create_file(
            src_pkg / "__main__.py",
            f"""\
from {package_name}.app.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
""",
            dry_run=dry_run,
        )
        create_file(
            src_pkg / "app" / "cli.py",
            """\
def main() -> int:
    print("CLI entrypoint")
    return 0
""",
            dry_run=dry_run,
        )

    if project_type == "service":
        create_file(
            src_pkg / "app" / "main.py",
            """\
def run() -> None:
    print("Service starting...")
""",
            dry_run=dry_run,
        )
        create_file(
            src_pkg / "infra" / "healthcheck.py",
            """\
def check() -> bool:
    return True
""",
            dry_run=dry_run,
        )

    # ------------------------------------------------------------------
    # tests/<package> mirrored layout
    # ------------------------------------------------------------------
    if not tests_root.exists():
        log("dir", tests_root, dry_run)
        if not dry_run:
            tests_root.mkdir(parents=True, exist_ok=True)

    if not tests_pkg.exists():
        log("dir", tests_pkg, dry_run)
        if not dry_run:
            tests_pkg.mkdir(parents=True, exist_ok=True)

    touch_init(tests_pkg / "core", dry_run=dry_run)

    if project_type in {"cli", "service"}:
        touch_init(tests_pkg / "app", dry_run=dry_run)

    if project_type == "service":
        touch_init(tests_pkg / "infra", dry_run=dry_run)

    # Root smoke test (kept simple, scales cleanly)
    create_file(
        tests_pkg / "test_smoke.py",
        "def test_smoke() -> None:\n    assert True\n",
        dry_run=dry_run,
    )

    # ------------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------------
    cleanup_legacy(root, dry_run=dry_run)

    mode = "DRY RUN" if dry_run else "CREATED"
    print(f"\n{mode}: initialized {project_type} project structure for '{package_name}'.")
    print(f"         updated pyproject.toml name to '{project_name}'")


if __name__ == "__main__":
    main()
