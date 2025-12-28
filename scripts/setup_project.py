import argparse
import re
import shutil
import sys
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
    new_content = re.sub(
        r"^(name\s*=\s*)([\"']).*?([\"'])",
        f"\\1\\2{new_name}\\3",
        content,
        flags=re.MULTILINE,
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


def create_src_layout(src_pkg: Path, project_type: str, dry_run: bool) -> None:
    touch_init(src_pkg, dry_run=dry_run)
    touch_init(src_pkg / "core", dry_run=dry_run)

    if project_type in {"cli", "service"}:
        touch_init(src_pkg / "app", dry_run=dry_run)

    if project_type == "service":
        touch_init(src_pkg / "infra", dry_run=dry_run)


def create_type_specific_files(
    src_pkg: Path, project_type: str, package_name: str, dry_run: bool
) -> None:
    if project_type == "library":
        create_file(
            src_pkg / "core" / "api.py", "# Public library API\n", dry_run=dry_run
        )

    if project_type == "cli":
        main_content = (
            f"from {package_name}.app.cli import main\n\n"
            'if __name__ == "__main__":\n'
            "    raise SystemExit(main())\n"
        )
        create_file(src_pkg / "__main__.py", main_content, dry_run=dry_run)
        create_file(
            src_pkg / "app" / "cli.py",
            'def main() -> int:\n    print("CLI entrypoint")\n    return 0\n',
            dry_run=dry_run,
        )

    if project_type == "service":
        create_file(
            src_pkg / "app" / "main.py",
            'def run() -> None:\n    print("Service starting...")\n',
            dry_run=dry_run,
        )
        create_file(
            src_pkg / "infra" / "healthcheck.py",
            "def check() -> bool:\n    return True\n",
            dry_run=dry_run,
        )


def create_tests_layout(
    tests_root: Path, tests_pkg: Path, project_type: str, dry_run: bool
) -> None:
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

    create_file(
        tests_pkg / "test_smoke.py",
        "def test_smoke() -> None:\n    assert True\n",
        dry_run=dry_run,
    )


def setup_environment(dry_run: bool) -> None:
    if not dry_run:
        print("\nInstalling pre-commit hooks...")
        try:
            import subprocess

            subprocess.run(["uv", "run", "pre-commit", "install"], check=True)
        except Exception as e:
            print(f"warning: failed to install pre-commit hooks: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize project structure.")
    parser.add_argument("--name", required=True, help="Python package name")
    parser.add_argument(
        "--type", required=True, choices=sorted(PROJECT_TYPES), help="Project type"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Print actions without execution"
    )

    args = parser.parse_args()
    package_name, project_type, dry_run = args.name, args.type, args.dry_run
    root = Path.cwd()
    src_pkg = root / "src" / package_name
    tests_root, tests_pkg = (
        root / "tests",
        root / "tests" / package_name,
    )

    if src_pkg.exists():
        die(f"Target package directory already exists: {src_pkg}")

    if not package_name.isidentifier():
        die(f"--name must be a valid Python identifier. Got: {package_name!r}")

    project_name = package_name.replace("_", "-")
    update_pyproject_name(project_name, dry_run=dry_run)
    create_src_layout(src_pkg, project_type, dry_run)
    create_type_specific_files(src_pkg, project_type, package_name, dry_run)
    create_tests_layout(tests_root, tests_pkg, project_type, dry_run)
    cleanup_legacy(root, dry_run=dry_run)
    setup_environment(dry_run)

    mode = "DRY RUN" if dry_run else "CREATED"
    print(
        f"\n{mode}: initialized {project_type} project structure for '{package_name}'."
    )
    print(f"         updated pyproject.toml name to '{project_name}'")


if __name__ == "__main__":
    main()
