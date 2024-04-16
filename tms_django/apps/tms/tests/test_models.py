from apps.tms.models import BookedLoad, Broker, DriverProfile, Truck, TruckKind
from django.test import TestCase


class TestTruckModel(TestCase):
    def setUp(self):
        self.truck = Truck.objects.create(kind=TruckKind.SMALL_STRAIGHT, weight=5000, capacity=2000)

    def test_truck_create(self):
        self.assertEqual(self.truck.kind, TruckKind.SMALL_STRAIGHT)
        self.assertEqual(self.truck.weight, 5000)
        self.assertEqual(self.truck.capacity, 2000)

    def test_truck_str(self):
        self.assertEqual(str(self.truck), "small straight")


class TestBrokerModel(TestCase):
    def setUp(self):
        self.broker = Broker.objects.create(agent_name="Angela K", company_name="Midex Corp")

    def test_broker_create(self):
        self.assertEqual(self.broker, Broker.objects.get())
