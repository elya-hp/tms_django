import factory
from apps.tms.tests.factories import DispatcherProfileFactory, DriverProfileFactory
from faker import Faker

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "users.User"
        django_get_or_create = ("username",)

    username = factory.Faker("user_name")
    email = factory.Faker("email")


class DispatcherUserFactory(UserFactory):
    profile = factory.RelatedFactory(DispatcherProfileFactory, factory_related_name="user")


class DriverUserFactory(UserFactory):
    profile = factory.RelatedFactory(DriverProfileFactory, factory_related_name="user")
