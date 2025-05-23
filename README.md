# <project name>

A template for Pythonic research software with environment management through `uv`.

## Post template copy instructions

While we provide some customizations to the files in this template based on your specification there's likely a chance some things aren't perfect.
We recommend taking a look at each file used within this template to ensure it meets your expectations for the project you're working on.
In addition, consider the following steps to help ensure the project is in good shape before proceeding too far.

- [ ] Remove files you plan on not using (e.g. `src/notebooks`, `.github/workflows/publish-pypi.yml`, etc.).
- [ ] Update the `LICENSE` file based on the project.
- [ ] Update the `CITATION.cff` file based on the project.
- [ ] Update the project dependencies using `uv remove` or `uv add`.
- [ ] Update the `pyproject.toml` file based on the project.
- [ ] Enable `pre-commit-lite` to help automate corrections to code during pull request updates. Otherwise, consider removing the step: labeled with: `pre-commit-ci/lite-action` within `.github/workflows/run-tests.yml`.
- [ ] Enable private security vulnerability issue reporting within the repo settings (e.g. https://github.com/repo_org/repo_name/settings/security_analysis)
- [ ] Enable branch protection rules to require one pull request review approval per pull request to help with maintainer expectations.
