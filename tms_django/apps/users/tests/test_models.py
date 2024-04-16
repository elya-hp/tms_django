from apps.users.tests.factories import DispatcherUserFactory, UserFactory
from django.test import TestCase


class TestUser(TestCase):
    def test__create(self):
        user = UserFactory()
        user.refresh_from_db()
        self.assertIsNotNone(user.id)


# TODO: test Dispatcher Profile
