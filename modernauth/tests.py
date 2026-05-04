from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import FieldDoesNotExist
from django.db import IntegrityError, transaction
from django.test import TestCase

from .models import User


class AuthTestCase(TestCase):
    def setUp(self):
        User.objects.create_superuser("admin@testproject.com", "pa55w0rd")
        User.objects.create_user("user@testproject.com", "pa55w0rd")

    def test_admin_created(self):
        self.assertTrue(User.objects.filter(email="admin@testproject.com").exists())

    def test_user_created(self):
        self.assertTrue(User.objects.filter(email="user@testproject.com").exists())

    def test_admin_email_is_username_field(self):
        admin = User.objects.get(email="admin@testproject.com")
        self.assertEqual("email", admin.USERNAME_FIELD)

    def test_user_email_is_username_field(self):
        user = User.objects.get(email="user@testproject.com")
        self.assertEqual("email", user.USERNAME_FIELD)

    def test_user_string_representation_is_email(self):
        user = User.objects.get(email="user@testproject.com")
        self.assertEqual(str(user), "user@testproject.com")

    def test_username_field_is_removed_from_model(self):
        with self.assertRaises(FieldDoesNotExist):
            User._meta.get_field("username")

    def test_get_user_model_resolves_to_modernauth_user(self):
        self.assertIs(get_user_model(), User)

    def test_auth_user_model_setting_points_at_modernauth(self):
        self.assertEqual(settings.AUTH_USER_MODEL, "modernauth.User")

    def test_email_domain_is_normalized_to_lowercase(self):
        # BaseUserManager.normalize_email lowercases the domain only.
        user = User.objects.create_user(email="bob@EXAMPLE.com", password="x")
        self.assertEqual(user.email, "bob@example.com")

    def test_email_local_part_is_lowercased(self):
        # The full email (local part + domain) is lowercased on save so that
        # identity is case-insensitive.
        user = User.objects.create_user(email="Alice@example.com", password="x")
        self.assertEqual(user.email, "alice@example.com")

    def test_save_lowercases_email_directly_assigned(self):
        # Defensive: even when the manager flow is bypassed and email is
        # directly assigned, save() must lowercase it before persisting.
        user = User.objects.create_user(email="someone@example.com", password="x")
        user.email = "MIXED@CASE.com"
        user.save()
        user.refresh_from_db()
        self.assertEqual(user.email, "mixed@case.com")

    def test_create_user_rejects_missing_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, password="x")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="x")

    def test_email_uniqueness_is_enforced(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            User.objects.create_user(email="user@testproject.com", password="x")

    def test_authenticate_with_correct_email_and_password_returns_user(self):
        user = authenticate(email="user@testproject.com", password="pa55w0rd")
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "user@testproject.com")

    def test_authenticate_with_wrong_password_returns_none(self):
        user = authenticate(email="user@testproject.com", password="WRONG")
        self.assertIsNone(user)

    def test_authenticate_is_case_insensitive_via_email_backend(self):
        user = authenticate(email="USER@TESTPROJECT.com", password="pa55w0rd")
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "user@testproject.com")

    def test_authenticate_with_wrong_password_via_email_backend(self):
        user = authenticate(email="USER@TESTPROJECT.com", password="WRONG")
        self.assertIsNone(user)

    def test_authenticate_inactive_user_returns_none(self):
        inactive = User.objects.create_user(
            email="inactive@testproject.com", password="pa55w0rd"
        )
        inactive.is_active = False
        inactive.save()
        user = authenticate(email="Inactive@TestProject.com", password="pa55w0rd")
        self.assertIsNone(user)

    def test_create_superuser_requires_is_staff_true(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email="x@x.com", password="x", is_staff=False)

    def test_create_superuser_requires_is_superuser_true(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="x@x.com", password="x", is_superuser=False
            )
