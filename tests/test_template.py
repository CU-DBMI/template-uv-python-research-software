"""
Tests the templating capabilities of the project.
"""

import os
import subprocess
from pathlib import Path

from copier import run_copy

# Common answers shared across template render tests. The Rust-bindings variant
# overrides ``use_rust`` to ``True``; answering it here keeps renders
# non-interactive.
_COMMON_DATA = {
    "project_name": "demo-project",
    "project_description": "A demo project for testing Copier templates.",
    "author_name": "Test Author",
    "author_orcid": "https://orcid.org/0000-0000-0000-0000",
    "github_url": "https://github.com/org/repo",
    "github_primary_reviewer": "@octocat",
    "use_rust": False,
}


def _git(*args: str, cwd: Path) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def _init_git_repo(path: Path) -> str:
    subprocess.run(["git", "init"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=path, check=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"], cwd=path, check=True
    )
    (path / "README.md").write_text("# Existing repo\n")
    subprocess.run(["git", "add", "README.md"], cwd=path, check=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=path, check=True)
    return _git("rev-parse", "HEAD", cwd=path)


def _commit_project(path: Path) -> None:
    subprocess.run(["git", "init"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=path, check=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"], cwd=path, check=True
    )
    subprocess.run(["git", "add", "."], cwd=path, check=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=path, check=True)


def _run_standalone_project_command(args: list[str], cwd: Path) -> None:
    env = os.environ.copy()
    env.pop("UV_RUN_RECURSION_DEPTH", None)
    env.pop("VIRTUAL_ENV", None)
    subprocess.run(args, cwd=cwd, check=True, env=env)


def test_template(tmp_path: Path) -> None:
    # Path to the Copier template root
    template_path = Path(__file__).resolve().parent.parent

    # Destination where the template will be copied
    dst_path = tmp_path / "copied"

    # Run Copier copy with default data (pure-Python variant)
    run_copy(
        src_path=str(template_path),
        dst_path=dst_path,
        data=_COMMON_DATA,
        quiet=True,
        overwrite=True,
        vcs_ref="HEAD",
    )

    # Assert a file from the template was created
    assert (dst_path / "src/demo_project/main.py").exists()
    assert (
        "zizmorcore/zizmor-pre-commit"
        in (dst_path / ".pre-commit-config.yaml").read_text()
    )
    assert (dst_path / ".github/zizmor.yml").exists()
    assert not (dst_path / ".git").exists()
    assert not (dst_path / "renovate.json").exists()

    # The pure-Python variant must not include any Rust bindings scaffolding
    assert not (dst_path / "Cargo.toml").exists()
    assert not (dst_path / "crates").exists()
    assert not (dst_path / "src/demo_project/api.py").exists()

    _commit_project(dst_path)

    # Verify the generated project exposes the documented pipeline without
    # nesting pre-commit hook environments inside this render test.
    _run_standalone_project_command(
        ["uv", "run", "--frozen", "poe", "--dry-run", "pipeline"],
        cwd=dst_path,
    )
    _run_standalone_project_command(
        ["uv", "run", "--frozen", "pytest"],
        cwd=dst_path,
    )


def test_template_rust(tmp_path: Path) -> None:
    template_path = Path(__file__).resolve().parent.parent
    dst_path = tmp_path / "copied-rust"

    # Run Copier copy opting into the Rust bindings
    run_copy(
        src_path=str(template_path),
        dst_path=dst_path,
        data={**_COMMON_DATA, "use_rust": True},
        quiet=True,
        overwrite=True,
        vcs_ref="HEAD",
    )

    # Rust bindings scaffolding is present
    assert (dst_path / "Cargo.toml").exists()
    assert (dst_path / "crates/demo_project_core/src/lib.rs").exists()
    assert (dst_path / "crates/demo_project_python/src/lib.rs").exists()
    assert (dst_path / "src/demo_project/api.py").exists()
    assert (dst_path / "src/demo_project/_native.pyi").exists()
    assert (dst_path / "tools/sync_release_version.py").exists()

    # Pure-Python-only content is excluded from the Rust variant
    assert not (dst_path / "src/demo_project/main.py").exists()
    assert not (dst_path / "src/notebooks").exists()

    _commit_project(dst_path)

    # Verify the generated Rust project exposes the documented pipeline without
    # nesting pre-commit hook environments inside this render test.
    _run_standalone_project_command(
        ["uv", "run", "--frozen", "poe", "--dry-run", "pipeline"],
        cwd=dst_path,
    )
    # The Rust unit tests, native build, and Python tests must all pass.
    _run_standalone_project_command(["cargo", "test"], cwd=dst_path)
    _run_standalone_project_command(
        ["uv", "run", "--frozen", "maturin", "develop"],
        cwd=dst_path,
    )
    _run_standalone_project_command(
        ["uv", "run", "--frozen", "pytest"],
        cwd=dst_path,
    )


def test_template_preserves_existing_git_repo(tmp_path: Path) -> None:
    template_path = Path(__file__).resolve().parent.parent
    dst_path = tmp_path / "existing-repo"
    dst_path.mkdir()
    original_head = _init_git_repo(dst_path)

    run_copy(
        src_path=str(template_path),
        dst_path=dst_path,
        data=_COMMON_DATA,
        quiet=True,
        overwrite=True,
        vcs_ref="HEAD",
    )

    assert (dst_path / "src/demo_project/main.py").exists()
    assert not (dst_path / "renovate.json").exists()
    assert _git("rev-parse", "--is-inside-work-tree", cwd=dst_path) == "true"
    assert _git("rev-parse", "HEAD", cwd=dst_path) == original_head
