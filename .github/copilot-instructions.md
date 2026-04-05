# Copilot Instructions

Trust these instructions. Only search the codebase if the information here is incomplete or found to be incorrect.

## Repository Summary

`fbm` is a Python tool project (purpose TBD — the package is currently a scaffold). The codebase is small: one source package (`src/fbm/`), one test file (`tests/test_import.py`), and standard Python project scaffolding.

- **Type**: Python library/tool
- **Python version**: >=3.11
- **Package manager**: `uv` (lockfile at `uv.lock`)
- **Build backend**: `setuptools` (src layout)
- **Test framework**: `pytest` + `pytest-cov`
- **Linter/formatter**: `ruff`

## Development Philosophy — TDD is Mandatory

**ALL development MUST follow Test-Driven Development:**

1. **Red** — Write a failing test that specifies the desired behavior. Run it and confirm it fails.
2. **Green** — Write the minimum production code needed to make the test pass. Run tests and confirm they pass.
3. **Refactor** — Improve code quality without changing behavior. Re-run tests to confirm still passing.

Never write production code without a failing test that requires it.

## Environment Setup

Always use `uv` for environment management. Do this once per machine/clone:

```powershell
# Create virtual environment (must be done first)
uv venv .venv

# Activate the virtual environment
.\.venv\Scripts\Activate.ps1

# Install the package and all dev dependencies (editable)
uv pip install -e .[dev]
```

> **Required**: The venv must be activated AND `uv pip install -e .[dev]` must have been run before any other commands will work. Without the editable install, `import fbm` fails.

## Build & Validate Commands

Run all commands from the repo root with the venv activated.

| Purpose | Command |
|---|---|
| Run tests | `uv run pytest -v` |
| Run tests with coverage | `uv run pytest --cov=fbm --cov-report=html` |
| Lint (check) | `uv run ruff check .` |
| Format (apply) | `uv run ruff format .` |
| Format (check only) | `uv run ruff format --check .` |

**Always run `uv run pytest -v` after making any change** to confirm the test suite still passes.

## Project Layout

```
pyproject.toml          # Project metadata, dependencies, build config
uv.lock                 # Locked dependency versions (commit this file)
README.md               # Quick start guide
.gitignore              # Ignores: __pycache__, .venv, .pytest_cache, htmlcov, *.egg-info, build, dist

src/
  fbm/
    __init__.py         # Package entry point; defines __version__ = "0.1.0"

tests/
  test_import.py        # Smoke test: verifies fbm.__version__ exists
```

- Source code lives under `src/fbm/`. All new modules go here.
- Tests live under `tests/`. Mirror the source structure (e.g., `src/fbm/foo.py` → `tests/test_foo.py`).
- No `conftest.py` exists yet. Create one at `tests/conftest.py` if shared fixtures are needed.
- `pyproject.toml` contains no `[tool.ruff]` or `[tool.pytest.ini_options]` sections yet; defaults are in effect.

## Dependency Management

- To add a runtime dependency: add to `[project]` `dependencies` in `pyproject.toml`, then run `uv pip install -e .[dev]`.
- To add a dev-only dependency: add to `[project.optional-dependencies]` `dev` list, then run `uv pip install -e .[dev]`.
- Always commit `uv.lock` after any dependency change.

## CI / Pre-commit Checks

There are no GitHub Actions workflows yet. The full manual validation sequence is:

```powershell
uv run ruff check .
uv run ruff format --check .
uv run pytest -v
```

All three must pass before a change is considered complete.

## Key Facts

- The `.venv/` directory is gitignored and must be recreated locally.
- `*.egg-info/` directories are gitignored but will appear under `src/` after editable install — this is expected.
- `htmlcov/` is gitignored; coverage reports are written there by `pytest --cov-report=html`.
- There is no `main` entry point or CLI yet.
- `ipython` is listed as a dev dependency for interactive exploration but is not required for tests or CI.
