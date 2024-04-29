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
    def test_truck_create(self):
        truck = TruckFactory()
        self.assertTrue(isinstance(truck, Truck))


class TestDriverModel(TestCase):
    def test_driver_create(self):
        driver = DriverProfileFactory()
        self.assertTrue(isinstance(driver, DriverProfile))


class TestDispatcherProfileModel(TestCase):
    def test_dispatcher_profile_create(self):
        dispatcher = DispatcherProfileFactory()
        self.assertTrue(isinstance(dispatcher, DispatcherProfile))


class TestBrokerModel(TestCase):
    def test_broker_create(self):
        broker = BrokerFactory()
        self.assertIsNotNone(broker.id)
        self.assertTrue(isinstance(broker, Broker))


class TestBookedLoadModel(TestCase):
    def test_booked_load_create(self):
        booked_load = BookedLoadFactory()
        self.assertTrue(isinstance(booked_load, BookedLoad))
