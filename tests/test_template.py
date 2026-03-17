"""
Tests the templating capabilities of the project.
"""

import subprocess
from pathlib import Path

from copier import run_copy


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


def test_template(tmp_path: Path) -> None:
    # Path to the Copier template root
    template_path = Path(__file__).resolve().parent.parent

    # Destination where the template will be copied
    dst_path = tmp_path / "copied"

    # Run Copier copy with default data (simulate user input)
    run_copy(
        src_path=str(template_path),
        dst_path=dst_path,
        data={
            "project_name": "demo-project",
            "project_description": "A demo project for testing Copier templates.",
            "author_name": "Test Author",
            "author_orcid": "https://orcid.org/0000-0000-0000-0000",
            "github_url": "https://github.com/org/repo",
        },
        quiet=True,
        overwrite=True,
        vcs_ref="HEAD",
    )

    # Assert a file from the template was created
    assert (dst_path / "src/demo_project/main.py").exists()
    assert not (dst_path / ".git").exists()

    # Run pytest from the copied template
    subprocess.run(["uv", "run", "pytest"], cwd=dst_path, check=True)


def test_template_preserves_existing_git_repo(tmp_path: Path) -> None:
    template_path = Path(__file__).resolve().parent.parent
    dst_path = tmp_path / "existing-repo"
    dst_path.mkdir()
    original_head = _init_git_repo(dst_path)

    run_copy(
        src_path=str(template_path),
        dst_path=dst_path,
        data={
            "project_name": "demo-project",
            "project_description": "A demo project for testing Copier templates.",
            "author_name": "Test Author",
            "author_orcid": "https://orcid.org/0000-0000-0000-0000",
            "github_url": "https://github.com/org/repo",
        },
        quiet=True,
        overwrite=True,
        vcs_ref="HEAD",
    )

    assert (dst_path / "src/demo_project/main.py").exists()
    assert _git("rev-parse", "--is-inside-work-tree", cwd=dst_path) == "true"
    assert _git("rev-parse", "HEAD", cwd=dst_path) == original_head
