"""
Tests the templating capabilities of the project.
"""

import subprocess
from pathlib import Path

from copier import run_copy


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

    # Run pytest from the copied template
    subprocess.run(["uv", "run", "pytest"], cwd=dst_path, check=True)
