from typing import Any

from django.contrib.auth.backends import ModelBackend
from django.http import HttpRequest

from .models import User

__all__ = ["EmailBackend"]


class EmailBackend(ModelBackend):
    """Authentication backend that performs case-insensitive email lookup.

    Companion to the ``User`` model's save-time lowercasing: because emails
    are stored lowercased, we lowercase the supplied credential before
    delegating to ``ModelBackend``. This lets a user who registered as
    ``alice@example.com`` log in by typing ``Alice@EXAMPLE.com`` without
    paying for a SQL ``LOWER(email)`` comparison on every authentication.
    """

    def authenticate(
        self,
        request: HttpRequest | None,
        username: str | None = None,
        password: str | None = None,
        **kwargs: Any,
    ) -> User | None:
        """Lowercase the email credential, then delegate to ``ModelBackend``.

        Django's auth machinery may pass the credential under either the
        ``username`` parameter (the historical default) or under a kwarg
        named after ``USERNAME_FIELD`` (``email`` here), depending on the
        form/view in play. We accept both, lowercase whichever was
        supplied, and let ``ModelBackend`` perform the natural-key lookup,
        password check, and ``user_can_authenticate`` (active) check.
        """
        username_field = User.USERNAME_FIELD
        if username is not None:
            username = username.lower()
        elif kwargs.get(username_field) is not None:
            kwargs[username_field] = kwargs[username_field].lower()
        else:
            return None
        return super().authenticate(
            request, username=username, password=password, **kwargs
        )
