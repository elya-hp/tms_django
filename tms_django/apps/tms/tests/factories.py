import factory
from apps.tms.models import BookedLoad, Truck, TruckKind
from factory import fuzzy
from faker import Faker

fake = Faker()


class TruckFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "tms.Truck"

    kind = factory.fuzzy.FuzzyChoice(TruckKind)
    weight = factory.Faker("random_number")
    capacity = factory.Faker("random_number")


class DriverProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "tms.DriverProfile"

    user = factory.SubFactory("apps.users.tests.factories.UserFactory")
    phone_number = factory.Faker("phone_number")
    driver_licence = factory.Faker("license_plate")
    date_of_birth = factory.Faker("date_of_birth")
    address = factory.Faker("address")
    truck = factory.SubFactory(TruckFactory)


class DispatcherProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "tms.DispatcherProfile"

    user = factory.SubFactory("apps.users.tests.factories.UserFactory")
    phone_number = factory.Faker("phone_number")


class BrokerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "tms.Broker"

    agent_name = factory.Faker("name")
    company_name = factory.Faker("company")
    mc_number = factory.Faker("license_plate")


class BookedLoadFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "tms.BookedLoad"

    status = factory.fuzzy.FuzzyChoice(BookedLoad.Status)
    driver = factory.SubFactory(DriverProfileFactory)
    pickup_location = factory.Faker("address")
    delivery_location = factory.Faker("address")
    distance = factory.Faker("random_number")
    pallets_quantity = factory.Faker("random_number")
    pallets_weight = factory.Faker("random_number")
    dispatcher = factory.SubFactory(DispatcherProfileFactory)
    broker = factory.SubFactory(BrokerFactory)
    total_rate = factory.Faker("random_number")
    driver_rate = factory.Faker("random_number")
