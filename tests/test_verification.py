"""Check all verification choices without expanding the interpreter matrix."""

import os
import subprocess
import tomllib
from pathlib import Path

import pytest
from copier import run_copy


@pytest.mark.parametrize("use_rust", [False, True])
@pytest.mark.parametrize("formal_verification", ["none", "lightweight", "advanced"])
def test_verification_options(
    tmp_path: Path, use_rust: bool, formal_verification: str
) -> None:
    """Render each option and keep verification separate from normal tests."""
    destination = tmp_path / "rendered"
    run_copy(
        str(Path(__file__).resolve().parent.parent),
        destination,
        data={
            "project_name": "demo-project",
            "project_description": "Verification render test.",
            "use_rust": use_rust,
            "formal_verification": formal_verification,
        },
        defaults=True,
        overwrite=True,
        quiet=True,
        vcs_ref="HEAD",
    )
    config = tomllib.loads((destination / "pyproject.toml").read_text())
    environment = os.environ.copy()
    environment["SETUPTOOLS_SCM_PRETEND_VERSION"] = "0.0.0"
    environment.pop("VIRTUAL_ENV", None)
    subprocess.run(
        ["uv", "lock", "--check"],
        cwd=destination,
        env=environment,
        check=True,
        timeout=120,
    )
    lock = tomllib.loads((destination / "uv.lock").read_text())
    packages = {package["name"] for package in lock["package"]}
    workflow_path = destination / ".github/workflows/formal-verification.yml"
    enabled = formal_verification != "none"
    assert workflow_path.exists() == enabled
    assert (destination / "verification").exists() == enabled
    assert (destination / "tests/test_index_contract.py").exists() == enabled
    assert not (destination / "tests/test_verification.py").exists()
    assert not (destination / "scripts/check_verification.py").exists()
    assert "formal-verification" in (destination / "AGENTS.md").read_text()
    assert (destination / ".agents/skills/formal-verification/SKILL.md").exists()
    assert ("hypothesis" in packages) == enabled
    assert ("crosshair-tool" in packages) == enabled
    assert ("verification" in config["dependency-groups"]) == enabled
    if enabled:
        workflow = workflow_path.read_text()
        assert "matrix:" not in workflow
        assert 'python-version: "3.11"' in workflow
        assert "--frozen" in workflow
        assert ("rust-verification:" in workflow) == use_rust
        assert ("cargo kani" in workflow) == use_rust
        assert "crosshair" in workflow
        inventory = (destination / "verification/README.md").read_text()
        assert "Example" in inventory
        assert ("## Advanced assessment" in inventory) == (
            formal_verification == "advanced"
        )
        verification = config["tool"]["uv"]["dependency-groups"]["verification"]
        assert verification["requires-python"] == ">=3.11,<3.12"
    if use_rust:
        core = destination / "crates/demo_project_core"
        source = (core / "src/lib.rs").read_text()
        assert ("#[kani::proof]" in source) == enabled
        if enabled:
            assert "count_primes(limit)" in source
            assert "kani::assume" in source
    else:
        assert not (destination / "crates").exists()
    normal_workflow = (destination / ".github/workflows/run-tests.yml").read_text()
    assert "crosshair" not in normal_workflow
    assert "cargo kani" not in normal_workflow
