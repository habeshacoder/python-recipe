"""
Test for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email, password=password)
        self.assertEqual(user.email == email, user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        emails = [
         ["Test@example.com", "test@example.com"],
         ['test@Example.com', 'test@example.com'],
         ['TEST@Example.com', 'test@example.com'],
         ['TEST@Example.COM', 'test@example.com'],
         ]

        for email, expected in emails:
            user = get_user_model().objects.create_user(email, 'testpass123')
            self.assertEqual(user.email, expected)

    def test_create_new_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'testpass123')
