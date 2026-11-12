"""Exercise generated verification commands on one supported interpreter."""

import argparse
import os
import subprocess
import tempfile
from pathlib import Path

from copier import run_copy


def main() -> None:
    """Render a project and run its verification without changing the template."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rust", action="store_true", help="Run the Rust harness.")
    args = parser.parse_args()
    environment = os.environ.copy()
    environment.pop("UV_RUN_RECURSION_DEPTH", None)
    environment.pop("VIRTUAL_ENV", None)
    # The throwaway render has no Git history for setuptools-scm.
    environment["SETUPTOOLS_SCM_PRETEND_VERSION"] = "0.0.0"
    with tempfile.TemporaryDirectory(prefix="template-verification-") as temporary:
        destination = Path(temporary) / "project"
        run_copy(
            str(Path(__file__).resolve().parent.parent),
            destination,
            data={
                "project_name": "verification-demo",
                "project_description": "Generated verification smoke test.",
                "formal_verification": "lightweight",
                "use_rust": args.rust,
            },
            defaults=True,
            overwrite=True,
            quiet=True,
            vcs_ref="HEAD",
        )
        commands = [["uv", "lock", "--check"]]
        if args.rust:
            commands.append(["cargo", "kani", "-p", "verification_demo_core"])
        else:
            runner = [
                "uv",
                "run",
                "--frozen",
                "--python",
                "3.11",
                "--only-group",
                "dev",
                "--only-group",
                "verification",
            ]
            commands.extend(
                [
                    [
                        *runner,
                        "pytest",
                        "-o",
                        "addopts=",
                        "tests/test_index_contract.py",
                    ],
                    [
                        *runner,
                        "crosshair",
                        "check",
                        "--report_all",
                        "--per_condition_timeout",
                        "10",
                        "verification/python/",
                    ],
                ]
            )
        for command in commands:
            print("Running:", " ".join(command), flush=True)
            subprocess.run(
                command, cwd=destination, env=environment, check=True, timeout=600
            )


if __name__ == "__main__":
    main()
