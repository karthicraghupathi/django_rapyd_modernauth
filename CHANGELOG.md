# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-05-04

### Added

- `User.save()` (and `create_user` / `create_superuser`) now lowercases `email`
  before writing, establishing a consistent storage invariant. Consumers upgrading
  from `0.0.x` should de-duplicate any mixed-case rows before upgrading — see the
  _Migration from 0.0.x_ section of the README.
- `modernauth.backends.EmailBackend` — a `ModelBackend` subclass that lowercases
  the supplied credential at authentication time, making login case-insensitive
  when wired into `AUTHENTICATION_BACKENDS`.

## [0.0.7] - 2026-05-04

### Fixed

- `publish.yml` now fires directly on `push: tags: ["v*"]`, bypassing the
  `GITHUB_TOKEN` cross-workflow chaining limitation that prevented OIDC publishing
  when triggered via a release event chain.

## [0.0.6] - 2026-05-04

### Added

- Django 5.2 LTS support alongside existing Django 4.2 LTS.
- Full type annotations across all public modules; `mypy` + `django-stubs` CI
  lint job added.
- `py.typed` marker (PEP 561) — the package now declares itself typed.
- `[dev]` optional-dependency extra (`pip install -e .[dev]` / `uv sync --all-extras`).
- `uv` as the dependency manager; `requirements-dev.txt` auto-exported from the
  lock file via a `pre-commit` hook.
- `pre-commit` with ruff, mypy, and uv-lock/uv-export hooks.
- `.editorconfig` for cross-IDE consistency.
- Dependabot configured for `pip`, `github-actions`, and `pre-commit` ecosystems.
- GitHub Actions CI: 7-combo Python × Django matrix, concurrency cancellation,
  packaging smoke test (wheel build + import verification).
- GitHub Actions publish workflow: OIDC trusted publishing (no API tokens).
- GitHub Actions release workflow: auto-creates a GitHub Release with
  auto-generated notes on tag push.
- `CONTRIBUTING.md` with dev setup, test workflow, and release process.
- `SECURITY.md` with vulnerability disclosure policy.

### Changed

- Migrated from `setup.py` + Pipfile to `pyproject.toml` as the single source of
  truth for metadata, build system, dependencies, and tool configuration.
- Migrated `flake8` + `isort` + `black` → `ruff` (lint + format).
- Migrated `bumpversion` config into `pyproject.toml` under `[tool.bumpversion]`
  (using `bump-my-version`).
- GitHub Actions first-party actions bumped to `v6`.
- Test suite expanded from 4 to 16 cases, covering the full model contract.

### Removed

- `setup.py`, `Makefile`, `setup_env.sh`, `Pipfile`, `Pipfile.lock` — superseded
  by `pyproject.toml` + `uv`.

## [0.0.5] - 2024-08-06

### Changed

- Additional compatibility fixes for Django 4 (follow-up to 0.0.4).

## [0.0.4] - 2022-08-27

### Changed

- Updated for Django 4 compatibility; removed calls to deprecated methods.

### Fixed

- Fleshed out installation instructions in the README.

## [0.0.3] - 2022-08-27

### Fixed

- Missing package included in distribution.
- Missing migrations included in package.
- Fixed `.env` file creation by properly quoting the Django secret key.

## [0.0.2] - 2022-01-23

### Added

- Author information; `logger` instance in the library.

## [0.0.1] - 2022-01-23

### Added

- Initial release: custom `User` model with `email` as the username field, no
  `username` field, and `UserManager` with `create_user` / `create_superuser`.
- Django admin integration via `UserAdmin`.

[Unreleased]: https://github.com/karthicraghupathi/django_rapyd_modernauth/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/karthicraghupathi/django_rapyd_modernauth/compare/v0.0.7...v0.1.0
[0.0.7]: https://github.com/karthicraghupathi/django_rapyd_modernauth/compare/v0.0.6...v0.0.7
[0.0.6]: https://github.com/karthicraghupathi/django_rapyd_modernauth/compare/v0.0.5...v0.0.6
[0.0.5]: https://github.com/karthicraghupathi/django_rapyd_modernauth/compare/v0.0.4...v0.0.5
[0.0.4]: https://github.com/karthicraghupathi/django_rapyd_modernauth/compare/v0.0.3...v0.0.4
[0.0.3]: https://github.com/karthicraghupathi/django_rapyd_modernauth/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/karthicraghupathi/django_rapyd_modernauth/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/karthicraghupathi/django_rapyd_modernauth/releases/tag/v0.0.1
