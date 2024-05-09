from apps.users.models import User
from apps.users.tests.factories import DispatcherUserFactory, UserFactory
from django.test import TestCase


class TestUser(TestCase):
    def test__create(self):
        user = UserFactory()
        user.refresh_from_db()
        self.assertIsNotNone(user.id)


class TestDispatcherUser(TestCase):
    model_cls = User

    def test__create(self):
        instance = DispatcherUserFactory()

        instance.refresh_from_db()
        self.assertTrue(isinstance(instance, User))
