### Repo Overview

- **Purpose**: Small Python utility `bg-remove` that currently contains a single script `main.py` and a minimal `pyproject.toml`. The project uses Python >= 3.13 and depends on `pillow` and `transparent-background` (see `pyproject.toml`).
- **Current shape**: single-module script (`main.py`) with an entry `main()` which prints a greeting. `README.md` is present but empty.

### What an AI coding agent should know first

- The codebase is intentionally minimal. Most changes will involve expanding from a script into a package, adding CLI, or integrating the `transparent-background` dependency.
- Key files:
  - `main.py` — simple entrypoint: `if __name__ == "__main__": main()`; modify here for quick demos.
  - `pyproject.toml` — declared `requires-python = ">=3.13"` and runtime dependencies. Keep this in sync when adding packages.
  - `README.md` — currently empty; updates here are acceptable and expected for usage instructions.

### Quick developer workflows (exact commands)

- Create and activate a virtualenv (macOS / zsh):
  ```bash
  python -m venv .venv
  source .venv/bin/activate
  python -m pip install --upgrade pip
  ```
- Install runtime dependencies quickly (recommended for development):
  ```bash
  pip install pillow transparent-background
  ```
- Run the small script:
  ```bash
  python main.py
  # or as a module
  python -m main
  ```
- Packaging notes: this repo has a `pyproject.toml` but no build-system table. If you add packaging/installation support, add a `[build-system]` section (e.g., `setuptools` or `poetry`) before relying on `pip install -e .`.

### Codebase conventions and patterns (project-specific)

- Single-file entrypoint for quick experiments. When adding features prefer converting to a package layout (`bg_remove/__init__.py`, `bg_remove/cli.py`) rather than growing `main.py` indefinitely.
- Keep `pyproject.toml` as the single source of truth for metadata and runtime deps. Update `dependencies` there when adding libraries.
- Tests: none currently. If adding tests, prefer `pytest` and add to `pyproject.toml` under a `[tool.pytest]` or include a `tox`/CI workflow.

### Integration points & external dependencies

- `transparent-background` is the primary external integration for background removal behavior. Treat it as a black-box library; document any wrapper code that normalizes inputs/outputs.
- Image handling uses `Pillow` — follow its conventions for `Image` objects and avoid converting to uncommon formats without explicit reason.

### When you create or modify behavior

- Small edits (example): to add a simple CLI flag for an input file, add `argparse` in `main.py` and keep the `main()` function as the program entry.
- Larger changes (example): when adding a new module or package, update `pyproject.toml` and the README with usage examples.

### What to preserve when merging existing AI guidance

- If a pre-existing `.github/copilot-instructions.md` or other agent docs exist, preserve any repository-specific examples, test/run commands, or important caveats about `pyproject.toml` and Python version.

### Small examples extracted from this repo

- Run the project: `python main.py` (see `main.py`).
- See declared deps: `pyproject.toml` includes `pillow>=12.0.0` and `transparent-background>=1.3.4`.

### Ask for clarification

If any runtime behavior, target platforms, or CI expectations are missing (for example, preferred packaging tool or test runner), ask the repository owner before making large structural changes.

---

If you'd like, I can (a) expand this file with a recommended package layout and example CLI implementation, or (b) add a minimal `pyproject` build-system section and `requirements-dev.txt`. Which would you prefer?
