"""Users Tests"""
from django.test import TestCase

# pylint: disable = no-name-in-module
from users.models import User


class TestUsers(TestCase):
    """Users Test"""

    # test creating a user
    def test_create_and_delete_user(self):
        """Test creating a user"""

        # create a user
        user = User.objects.create_user(
            phone_number="1234567890",
            password="password",
            username="testuser",
            first_name="test",
            last_name="user",
            email="testuser@bowspace.com",
            role="STUDENT",
            enrolled_courses={},
            ongoing_session={}
        )

        # assert that the user is created
        self.assertEqual(user.phone_number, "1234567890")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.first_name, "test")
        self.assertEqual(user.last_name, "user")
        self.assertEqual(user.email, "testuser@bowspace.com")
        self.assertEqual(user.role, "STUDENT")
        self.assertEqual(user.enrolled_courses, {})
        self.assertEqual(user.ongoing_session, {})
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        # delete the user
        user.delete()

        # assert that the user is deleted
        self.assertFalse(User.objects.filter(phone_number="1234567890").exists())
        return None
    
    