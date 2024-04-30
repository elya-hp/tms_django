from pprint import pprint

from apps.tms.models import (
    BookedLoad,
    Broker,
    DispatcherProfile,
    DriverProfile,
    Truck,
    TruckKind,
)
from apps.tms.tests.factories import (
    BookedLoadFactory,
    BrokerFactory,
    DispatcherProfileFactory,
    DriverProfileFactory,
    TruckFactory,
)
from django.test import TestCase


class TestTruckModel(TestCase):
    model_cls = Truck

    def test_factory(self):
        instance = TruckFactory()

        instance.refresh_from_db()
        self.assertIsInstance(instance, self.model_cls)
        self.assertIsNotNone(instance.id)


# TODO: update tests below (as TestTruckModel) so that they are structured in the same way:


class TestDriverModel(TestCase):
    def test_driver_create(self):
        driver = DriverProfileFactory()
        self.assertTrue(isinstance(driver, DriverProfile))
        # todo: make sure [user, truck] object(s) are created


class TestDispatcherProfileModel(TestCase):
    def test_dispatcher_profile_create(self):
        dispatcher = DispatcherProfileFactory()
        self.assertTrue(isinstance(dispatcher, DispatcherProfile))
        # todo: make sure [user] object(s) are created


class TestBrokerModel(TestCase):
    def test_broker_create(self):
        broker = BrokerFactory()
        self.assertIsNotNone(broker.id)
        self.assertTrue(isinstance(broker, Broker))


class TestBookedLoadModel(TestCase):
    def test_booked_load_create(self):
        booked_load = BookedLoadFactory()
        self.assertTrue(isinstance(booked_load, BookedLoad))
        # todo: make sure all related object(s) are created
