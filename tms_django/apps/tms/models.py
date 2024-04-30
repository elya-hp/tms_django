from apps.tms.generators import generate_load_id, generate_unit_id
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import OperationalError, models
from django.utils.translation import gettext_lazy as _
from loguru import logger


class TruckKind(models.TextChoices):
    SPRINTER = "sprinter"
    SMALL_STRAIGHT = "small_straight"
    LARGE_STRAIGHT = "large_straight"


class Truck(models.Model):
    kind = models.CharField(choices=TruckKind, max_length=255)
    weight = models.IntegerField(null=True, default=None, validators=[MinValueValidator(0)])
    capacity = models.IntegerField(null=True, default=None, validators=[MinValueValidator(0)])

    def __str__(self) -> str:
        return f"{self.kind} id={self.id}"


class DriverProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="driver_profile", on_delete=models.CASCADE)
    unit_id = models.CharField(max_length=6, unique=True, db_index=True, default=generate_unit_id)
    phone_number = models.CharField(max_length=255, blank=False)
    driver_licence = models.CharField(max_length=255, blank=False)
    date_of_birth = models.DateField(null=True, blank=False)
    address = models.CharField(max_length=255)
    truck = models.ForeignKey(Truck, null=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"unit_id={self.unit_id}"


class DispatcherProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="dispatcher_profile", on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"id={self.id}"


class Broker(models.Model):
    agent_name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=50)
    mc_number = models.CharField(max_length=10)
    # TODO add more details (broker MC)

    def __str__(self) -> str:
        return f"{self.agent_name} from {self.company_name}, id={self.id}"


class BookedLoad(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", _("PENDING")
        HEADING_TO_THE_PICKUP = "heading_to_the_pickup", _("HEADING_TO_THE_PICKUP")
        LOADING = "loading", _("LOADING")
        ON_ROUTE = "on_route", _("ON_ROUTE")
        UNLOADING = "unloading", _("UNLOADING")
        DELIVERED = "delivered", _("DELIVERED")
        INVOICED = "invoiced", _("INVOICED")
        CANCELLED = "cancelled", _("CANCELLED")
        COMPLETED = "completed", _("COMPLETED")
        VOIDED = "voided", _("VOIDED")

    load_id = models.CharField(max_length=6, unique=True, db_index=True, default=generate_load_id)
    status = models.CharField(choices=Status, max_length=255)
    driver = models.ForeignKey("tms.DriverProfile", on_delete=models.CASCADE)
    pickup_location = models.CharField(max_length=30)
    delivery_location = models.CharField(max_length=30)
    distance = models.IntegerField(null=True, default=None, validators=[MinValueValidator(0)])
    pallets_quantity = models.IntegerField(null=True, default=None, validators=[MinValueValidator(0)])
    pallets_weight = models.IntegerField(null=True, default=None, validators=[MinValueValidator(0)])
    dispatcher = models.ForeignKey("tms.DispatcherProfile", on_delete=models.CASCADE)
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE)
    total_rate = models.IntegerField(default=None)
    driver_rate = models.IntegerField(default=None)
    invoice_id = models.CharField(max_length=8, unique=True, db_index=True, default=None, null=True)

    def __str__(self) -> str:
        return f"load_id={self.load_id} [{self.status}]"


class Billing(BookedLoad):
    class Meta:
        proxy = True
        verbose_name_plural = "Billing"
