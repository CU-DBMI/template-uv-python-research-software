# template-uv-python-research-software

[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-orange.json)](https://github.com/copier-org/copier)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Software DOI badge](https://zenodo.org/badge/DOI/10.5281/zenodo.15518401.svg)](https://doi.org/10.5281/zenodo.15518401)

This is a [`copier`](https://github.com/copier-org/copier) template for building Python research software through the `uv` environment manager.

## Using this template

Follow these steps to use this template:

1. [Install `copier`](https://copier.readthedocs.io/en/stable/#installation) (e.g. `pip install copier`).
1. Reference this repository through the `copier copy <source> <target>` command. (e.g. `copier copy https://github.com/cu-dbmi/template-uv-python-research-software destination_path`)
1. Follow the directions in your new repo's `README.md` and make sure to check each file for alignment with your project.
1. Enjoy!

## What's included in the template

- Pre-configured `pyproject.toml` for Python project management
- Support for the [`uv`](https://github.com/astral-sh/uv) environment manager
- Example source code and test structure
- Example docs structure with the option to publish to GitHub Pages
- Ready-to-use GitHub Actions CI workflow (including tests, docs, and deployment)
- Community health files like LICENSE, CODE_OF_CONDUCT, and CONTRIBUTING with boilerplate language
- Support for Jupyter notebook development alongside a local Python package
- `.pre-commit-config.yaml` which can help with pre-commit checks for your project
- Adds a CLI boilerplate to build from based on `fire`.

## Post-copy guidance

Please reference the `README.md` checklist for suggested next steps after copying the template.
When using the Jupyter notebook work, consider using `uv run jupyter lab` (or similar) to run notebooks which are invoked from the context of the virtual environment of the project.
This helps the notebook gain dependencies and access to the packaged work outside the notebooks directory.

## Development

This project is a [Copier](https://copier.readthedocs.io/) template repository, designed to scaffold new projects using customizable templates.
The templates leverage [Jinja](https://jinja.palletsprojects.com/) for flexible variable substitution and logic within template files.

To ensure the template remains functional and testable, [pytest](https://pytest.org/) is used.
Tests are provided to verify that the template can be rendered and instantiated correctly, helping to catch issues early in the development process.

For example, use the following to test the work:

```bash
uv run pytest
```
