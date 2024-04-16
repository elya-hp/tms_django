import factory
from faker import Faker

fake = Faker()


class DispatcherProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "tms.DispatcherProfile"

    phone_number = factory.Faker("phone_number")
