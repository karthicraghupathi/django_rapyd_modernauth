# Django Rapyd ModernAuth

[![PyPI version](https://img.shields.io/pypi/v/django-rapyd-modernauth.svg)](https://pypi.org/project/django-rapyd-modernauth/)
[![Python versions](https://img.shields.io/pypi/pyversions/django-rapyd-modernauth.svg)](https://pypi.org/project/django-rapyd-modernauth/)
[![License](https://img.shields.io/pypi/l/django-rapyd-modernauth.svg)](LICENSE)
[![CI](https://github.com/karthicraghupathi/django_rapyd_modernauth/actions/workflows/test.yml/badge.svg)](https://github.com/karthicraghupathi/django_rapyd_modernauth/actions/workflows/test.yml)

A small Django pluggable app that provides a custom `User` model where the **email address is the username**. No `username` field, no extra settings, no migrations beyond the initial one.

## Inspiration

Users today expect to use their email address as the username during authentication. This works well because:

- Users already know their email addresses by heart.
- Since email addresses are unique, users don't need to remember yet another item when either signing up or logging into web applications. IMHO this is a significant factor that plays a vital role in user adoption.
- This is a time tested model and many web applications today follow this.

However, Django's default approach for authentication requires a user provide both a username and an email address during sign up and then just use the username during login.

## Requirements

- Python 3.10, 3.11, 3.12, or 3.13
- Django 4.2 LTS or Django 5.2 LTS

## Installation

> **Important:** swap in this user model **before** running `migrate` for the first time. Switching `AUTH_USER_MODEL` mid-project requires hand-written data migrations across every foreign key to the user model. See [Django's docs on substituting a custom user model](https://docs.djangoproject.com/en/stable/topics/auth/customizing/#substituting-a-custom-user-model).

Install the package:

```bash
pip install django-rapyd-modernauth
```

Add `modernauth` to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    "modernauth",
]
```

Point Django at the custom user model in `settings.py`:

```python
AUTH_USER_MODEL = "modernauth.User"
```

Create the database tables:

```bash
python manage.py migrate
```

## Usage

The custom `User` model behaves like Django's default `AbstractUser` with one difference: `email` is the unique identifier and there is no `username` field. Use `get_user_model()` rather than importing the model directly so your code keeps working if `AUTH_USER_MODEL` is ever swapped again.

```python
from django.contrib.auth import get_user_model

User = get_user_model()

User.objects.create_user(email="alice@example.com", password="…")
User.objects.create_superuser(email="root@example.com", password="…")
```

The admin's `createsuperuser` command will prompt for an email instead of a username:

```bash
python manage.py createsuperuser
```

Login forms, the admin, and `authenticate()` all use `email` as the credential.

## Contributing

Pull requests are welcome. The project is intentionally small — the goal is "swap the username field, nothing more" — so feature additions outside that scope are unlikely to land. Bug fixes, test improvements, and Django LTS support updates are always welcome.

### Development setup

```bash
git clone git@github.com:karthicraghupathi/django_rapyd_modernauth.git
cd django_rapyd_modernauth
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install python-dotenv tox bump-my-version build twine
echo "DJANGO_SECRET_KEY=local-dev-secret" > .env
```

The `.env` file is required by the bundled test project's settings module (it loads `DJANGO_SECRET_KEY` via `python-dotenv`) and is gitignored. `python-dotenv` is a test-time dependency only — it is not installed by the package itself.

### Running tests

The fast inner loop:

```bash
python testrunner.py
```

The full LTS × Python matrix is driven by tox. With [asdf](https://asdf-vm.com/) (or any tool that exposes `python3.10` through `python3.13` on `PATH`) installed:

```bash
tox p     # parallel
```

The matrix covers:

| | Django 4.2 LTS | Django 5.2 LTS |
|---|---|---|
| Python 3.10 | ✓ | ✓ |
| Python 3.11 | ✓ | ✓ |
| Python 3.12 | ✓ | ✓ |
| Python 3.13 | — (4.2 does not support 3.13) | ✓ |

The same matrix runs in CI on every push and pull request — see [`.github/workflows/test.yml`](.github/workflows/test.yml).

### Releasing

Releases are cut with [`bump-my-version`](https://github.com/callowayproject/bump-my-version), which manages the version string in `pyproject.toml` and `modernauth/__init__.py` in lockstep and creates a `v`-prefixed git tag. The configuration lives under `[tool.bumpversion]` in `pyproject.toml`.

```bash
# 1. Confirm tree is clean and tox is green
git status
tox p

# 2. Bump the version (creates the version commit + git tag automatically)
bump-my-version bump patch       # 0.0.6 → 0.0.7  (bug-fix release)
bump-my-version bump minor       # 0.0.6 → 0.1.0  (Django LTS support changes, etc.)
bump-my-version bump major       # 1.0.0 → 2.0.0  (breaking)

# 3. Push commit + tag
git push origin main --follow-tags

# 4. Build and upload to PyPI
python -m build
twine upload dist/*
```

Use `bump-my-version bump <part> --dry-run --verbose` to see exactly which files and lines would change before committing.

## License

Apache License 2.0 — see [LICENSE](LICENSE).
