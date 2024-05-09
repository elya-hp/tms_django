from apps.tms.generators import generate_model_custom_id
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
from loguru import logger


class TestIdGenerator(TestCase):
    def test_generate_model_custom_id__no_records(self):
        self.assertFalse(DriverProfile.objects.all().exists(), "clean your DriverProfile db records")
        default_value = 101
        expected = str(default_value)

        result = generate_model_custom_id(
            model_name="DriverProfile",
            custom_id_field_name="unit_id",
            default_value=default_value,
        )
        self.assertEqual(result, expected)

    def test_generate_model_custom_id__with_records(self):
        dp1 = DriverProfileFactory()
        dp2 = DriverProfileFactory()
        logger.info(f"{dp1}, {dp2}")
        expected = str(int(dp2.unit_id) + 1)

        result = generate_model_custom_id(
            model_name="DriverProfile",
            custom_id_field_name="unit_id",
            default_value=1000,
        )

        self.assertEqual(result, expected)


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
        self.assertIsInstance(instance, self.model_cls)
        self.assertIsInstance(instance.user, User)
        self.assertIsInstance(instance.truck, Truck)
        self.assertIsNotNone(instance.id)


class TestDispatcherProfileModel(TestCase):
    model_cls = DispatcherProfile

    def test_factory(self):
        instance = DispatcherProfileFactory()

        instance.refresh_from_db()
        self.assertIsInstance(instance, self.model_cls)
        self.assertIsInstance(instance.user, User)


class TestBrokerModel(TestCase):
    model_cls = Broker

    def test_factory(self):
        instance = BrokerFactory()

        instance.refresh_from_db()
        self.assertIsInstance(instance, self.model_cls)
        self.assertIsNotNone(instance.id)


class TestBookedLoadModel(TestCase):
    model_cls = BookedLoad

    def test_factory(self):
        instance = BookedLoadFactory()

        instance.refresh_from_db()
        self.assertIsInstance(instance, self.model_cls)
        self.assertIsInstance(instance.driver, DriverProfile)
        self.assertIsInstance(instance.dispatcher, DispatcherProfile)
        self.assertIsInstance(instance.broker, Broker)
        self.assertIsNotNone(instance.load_id)
        self.assertIsNotNone(instance.invoice_id)
