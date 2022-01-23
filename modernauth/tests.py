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
