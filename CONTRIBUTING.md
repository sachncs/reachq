# Contributing to reachq

Thank you for considering contributing to reachq. This document describes how
to set up your environment, run the tests, and open a pull request.

## Table of contents

- [Code of conduct](#code-of-conduct)
- [Getting started](#getting-started)
- [Development setup](#development-setup)
- [Branch naming](#branch-naming)
- [Commit conventions](#commit-conventions)
- [Pull request process](#pull-request-process)
- [Coding standards](#coding-standards)
- [Running tests](#running-tests)
- [Documentation](#documentation)
- [Docstring pitfall: avoid `O(...)`-looking tokens](#docstring-pitfall-avoid-o-looking-tokens)

## Code of conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md). By
participating, you agree to uphold it.

## Getting started

1. **Fork** the repository on GitHub.
2. **Clone** your fork locally:

    ```bash
    git clone https://github.com/<your-username>/reachq.git
    cd reachq
    ```

3. **Add the upstream remote**:

    ```bash
    git remote add upstream https://github.com/sachncs/reachq.git
    ```

## Development setup

### Prerequisites

- Python >= 3.10
- `pip` or an equivalent package manager

### Installation

```bash
# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in editable mode with development dependencies
pip install -e ".[dev]"

# Verify installation
pytest
```

### Code quality tools

This project uses:

- **ruff** for linting and formatting
- **mypy** for static type checking
- **pytest** for testing

Run all checks before opening a pull request:

```bash
ruff check reachq tests scripts
mypy reachq
pytest
```

## Branch naming

Use a descriptive prefix:

| Prefix | Purpose |
| ------ | ------- |
| `feat/` | New feature |
| `fix/` | Bug fix |
| `docs/` | Documentation only |
| `refactor/` | Refactor without behaviour change |
| `test/` | New or updated tests |
| `chore/` | Maintenance |

Examples:

- `feat/add-parallel-bfs`
- `fix/shortcut-set-edge-case`
- `docs/update-api-reference`

## Commit conventions

This project follows [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Types

- **feat**: a new feature.
- **fix**: a bug fix.
- **docs**: documentation only.
- **style**: code style (formatting, missing semicolons).
- **refactor**: a change that neither fixes a bug nor adds a feature.
- **test**: new or updated tests.
- **chore**: build process or auxiliary tools.

### Examples

```
feat(graph): add weighted graph support
fix(hopset): correct distance calculation for edge case
docs(api): update function signatures
refactor(reachability): simplify BFS implementation
test(shortcut_set): add invariant checking tests
chore(ci): update GitHub Actions workflow
```

### Scopes

`graph`, `reachability`, `shortest-paths`, `shortcut-set`, `hopset`,
`transitive-closure`, `generators`, `serialization`, `work-depth`, `invariants`,
`cli`, `ci`.

## Pull request process

### Before submitting

1. Ensure your code passes all checks:

    ```bash
    ruff check reachq tests scripts
    mypy reachq
    pytest
    ```

2. Update the documentation if your change affects the public API.
3. Add an entry to `CHANGELOG.md` under `[Unreleased]`.
4. Rebase on the latest `master` branch.

### PR title

Use the same convention as commit messages:

```
feat(reachability): add parallel BFS with shortcut edges
```

### PR description

Include:

- **Summary**: what the PR does.
- **Related issue**: link to the issue (if applicable).
- **Changes**: bullet list.
- **Testing**: how you tested it.
- **Checklist**: see below.

### Checklist

- [ ] Code follows the project's coding standards.
- [ ] Tests pass locally (`pytest`).
- [ ] Linting passes (`ruff check`).
- [ ] Type checking passes (`mypy reachq`).
- [ ] Documentation is updated (if applicable).
- [ ] `CHANGELOG.md` is updated under `[Unreleased]`.
- [ ] Commit messages follow Conventional Commits.

## Coding standards

### General

- Target Python >= 3.10.
- Use type hints on all public functions.
- Follow Google-style docstrings (enforced by `ruff`).
- Keep lines under 100 characters.

### Graph algorithms

- Accept `random_seed` parameters for reproducibility.
- Use `random.Random` instances, not the global `random`.
- Document asymptotic complexity in docstrings.
- Mark theoretical assumptions with `ASSUMPTION` comments.

### Testing

- Write tests for all new public functions.
- Use `pytest` markers: `@pytest.mark.slow` for expensive tests.
- Include both positive and negative test cases.
- Cover edge cases (empty graphs, single vertex, and so on).

## Running tests

```bash
# All tests
pytest

# With coverage
pytest --cov=reachq --cov-report=term-missing

# Skip slow tests
pytest -m "not slow"

# A specific test file
pytest tests/test_reachability.py

# Verbose
pytest -v
```

## Documentation

- Update `docs/` when you add a new module or function.
- Keep `README.md` focused on getting started.
- Add an example for every new public API.
- Document breaking changes in `CHANGELOG.md`.

## Questions?

Open an issue with the label `question` if you need help getting started.

## Docstring pitfall: avoid `O(...)`-looking tokens

`pyproject.toml` enables pytest's `--doctest-modules` flag, which runs every
module's docstring through Python's doctest parser. The parser is greedy: any
line that looks like a Python expression (for example `O(n^2)`, `n*rho`,
`O(beta)`) is attempted, and expressions that fail to evaluate break the
collection of an entire test file.

When you document complexity, choose one of:

- Write the symbol in prose: "quadratic", "linear in n", "cubic in the edge count".
- Use a backtick-quoted form: `` `O(n^2)` ``.
- Use a different symbol: ``Theta(n^2)``, ``Big-O(n^2)``, ``n^2``.

The `tests/test_docstring_no_doctest_collision.py` regression test greps every
docstring in `reachq/` for collision-prone patterns. Keep it passing.