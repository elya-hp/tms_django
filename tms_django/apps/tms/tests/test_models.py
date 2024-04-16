from apps.tms.models import BookedLoad, Broker, DriverProfile, Truck, TruckKind
from django.test import TestCase


class TestTruckModel(TestCase):
    def test_truck_create(self):
        truck = Truck.objects.create(kind=TruckKind.SMALL_STRAIGHT, weight=5000, capacity=2000)
        self.assertEqual(truck.kind, TruckKind.SMALL_STRAIGHT)
        self.assertEqual(truck.weight, 5000)
        self.assertEqual(truck.capacity, 2000)


class TestBrokerModel(TestCase):
    def test_broker_create(self):
        broker = Broker.objects.create(agent_name="Angela K", company_name="Midex Corp")
        self.assertIsNotNone(broker.id)
