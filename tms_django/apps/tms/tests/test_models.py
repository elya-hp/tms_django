from apps.tms.models import BookedLoad, Broker, DispatcherProfile, DriverProfile, Truck
from apps.tms.tests.factories import (
    BookedLoadFactory,
    BrokerFactory,
    DispatcherProfileFactory,
    DriverProfileFactory,
    TruckFactory,
)
from apps.users.models import User
from django.test import TestCase


class TestTruckModel(TestCase):
    model_cls = Truck

    def test_factory(self):
        instance = TruckFactory()

        instance.refresh_from_db()
        self.assertIsInstance(instance, self.model_cls)
        self.assertIsNotNone(instance.id)


class TestDriverModel(TestCase):
    model_cls = DriverProfile

    def test_factory(self):
        instance = DriverProfileFactory()

        instance.refresh_from_db()
        self.assertTrue(instance, self.model_cls)
        self.assertTrue(isinstance(instance.user, User))
        self.assertTrue(isinstance(instance.truck, Truck))


class TestDispatcherProfileModel(TestCase):
    model_cls = DispatcherProfile

    def test_factory(self):
        instance = DispatcherProfileFactory()

        instance.refresh_from_db()
        self.assertTrue(isinstance(instance, self.model_cls))
        self.assertTrue(isinstance(instance.user, User))


class TestBrokerModel(TestCase):
    model_cls = Broker

    def test_factory(self):
        instance = BrokerFactory()

        instance.refresh_from_db()
        self.assertIsNotNone(instance.id)
        self.assertTrue(isinstance(instance, self.model_cls))


class TestBookedLoadModel(TestCase):
    model_cls = BookedLoad

    def test_factory(self):
        instance = BookedLoadFactory()
        self.assertTrue(isinstance(instance, self.model_cls))
        self.assertTrue(isinstance(instance.status, BookedLoad.Status))
        self.assertTrue(isinstance(instance.driver, DriverProfile))
        self.assertTrue(isinstance(instance.dispatcher, DispatcherProfile))
        self.assertTrue(isinstance(instance.broker, Broker))

