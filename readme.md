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

Optionally enable case-insensitive login by adding the `EmailBackend` to your `AUTHENTICATION_BACKENDS`:

```python
AUTHENTICATION_BACKENDS = [
    "modernauth.backends.EmailBackend",
]
```

This is optional but recommended. Emails are stored lowercased on save, so the backend lowercases the credential at login time and matches against stored values — meaning `Alice@Example.com` and `alice@example.com` resolve to the same account. Without it, Django's default `ModelBackend` will only match if the consumer's login form lowercases the input first.

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

Emails are normalized to lowercase whenever a user is created or saved, so the address is the canonical identity. With the `EmailBackend` enabled (see [Installation](#installation)), `authenticate()` lowercases the supplied credential before lookup, making login case-insensitive.

## Migration from 0.0.x

Starting in 0.1.0 the package's behavior changed in two ways:

- `User.save()` (and therefore `create_user` / `create_superuser`) lowercases `email` before writing.
- The new `modernauth.backends.EmailBackend` lowercases the supplied credential at authentication time, making login case-insensitive when wired into `AUTHENTICATION_BACKENDS`.

The public API surface is unchanged — same model, same manager methods — but consumers upgrading from `0.0.x` should be aware of the points below.

### Existing data is not retroactively normalized

This package does **not** rewrite existing rows. New writes go through the lowercasing path, but rows that already exist with mixed-case local parts (e.g. `Alice@example.com`) stay as-is until the consumer migrates them. If you want the storage invariant to hold across the whole table, you need to run a one-shot data migration in your own project.

### Risk: unique-constraint conflicts

Under the old behavior the unique index on `email` was byte-comparison, so it was possible to have both `Alice@example.com` and `alice@example.com` as separate users. A naive lowercasing migration will fail on the duplicate. **De-dup first**, then migrate.

### Suggested data migration

The sketch below is a starting point, not a turnkey solution. Put it in a data migration in your own project (we don't ship one):

```python
# Sketch: in your project, create a data migration that lowercases existing emails.
def lowercase_emails(apps, schema_editor):
    User = apps.get_model("modernauth", "User")
    for user in User.objects.all():
        lowered = user.email.lower()
        if user.email != lowered:
            # Caller is responsible for de-duping conflicts before running this.
            user.email = lowered
            user.save(update_fields=["email"])
```

### Rolling back

If you don't want this behavior, pin to the last release before the change:

```bash
pip install "django-rapyd-modernauth<0.1.0"
```

## Contributing

Pull requests are welcome — the project is intentionally small, so bug fixes, test improvements, and Django LTS support updates are the most likely to land. See [CONTRIBUTING.md](CONTRIBUTING.md) for the full development setup, test workflow, and release process. See [CHANGELOG.md](CHANGELOG.md) for version history.

For security vulnerabilities, see [SECURITY.md](SECURITY.md) for the private disclosure process. **Do not file a public issue for security bugs.**

## License

Apache License 2.0 — see [LICENSE](LICENSE).
