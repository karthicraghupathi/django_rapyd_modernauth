# Django Rapyd ModernAuth

This package provides a custom `User` model where the username is the email address.

## Inspiration

Users today expect to use their email address as the username during authentication. This works well because:

- Users already know their email addresses by heart.
- Since email addresses are unique, users don't need to remember yet another item when either signing up or logging into web applications. IMHO this is a significant factor that plays a vital role in user adoption.
- This is a time tested model and many web applications today follow this.

However, Django's default approach for authentication requires a user provide both a username and an email address during sign up and then just use the username during login.

## Usage

**Note:** *Django recommends you do this right at the beginning of the project. Making this change mid-project becomes significantly harder.*

- Install the package with:
  ```commandline
  pip install django-rapyd-modernauth
  ```
- Edit Django settings:
  - Add `modernauth` to `INSTALLED_APPS`.
    ```python
    INSTALLED_APPS = [
        ...
        ...
        "modernauth",
    ]
    ```
  - Set `modernauth.User` as the `AUTH_USER_MODEL`.
    ```python
    AUTH_USER_MODEL = "modernauth.User"
    ```
- Create models with:
  ```commandline
  ./manage.py migrate
  ```
