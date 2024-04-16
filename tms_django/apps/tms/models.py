from __future__ import annotations

from functools import partial

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MinValueValidator
from django.db import OperationalError, models
from django.utils.translation import gettext_lazy as _
from loguru import logger


def generate_model_custom_id(model_name: str, custom_id_field_name: str, default_value: int) -> str:
    model = apps.get_model(app_label="tms", model_name=model_name)

    try:
        instance = model.objects.order_by("-id")[:1].get()
    except (OperationalError, ObjectDoesNotExist):
        logger.info(f"No record found for {model_name}, setting {default_value=}")
        last_custom_id = default_value

    else:
        last_custom_id = getattr(instance, custom_id_field_name)
        logger.info(f"Last id for {model_name}: {last_custom_id}")
        last_custom_id = int(last_custom_id) + 1

    return str(last_custom_id)


class TruckKind(models.TextChoices):
    SPRINTER = "sprinter"
    SMALL_STRAIGHT = "small straight"
    LARGE_STRAIGHT = "large straight"


class Truck(models.Model):
    kind = models.CharField(choices=TruckKind, max_length=255)
    weight = models.IntegerField(null=True, default=None, validators=[MinValueValidator(0)])
    capacity = models.IntegerField(null=True, default=None, validators=[MinValueValidator(0)])

    def __str__(self) -> str:
        return f"{self.kind}"


generate_unit_id = partial(
    generate_model_custom_id, model_name="DriverProfile", custom_id_field_name="unit_id", default_value=1000
)


class DriverProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="driver_profile", on_delete=models.CASCADE)
    unit_id = models.CharField(max_length=6, unique=True, db_index=True, default=generate_unit_id)
    truck = models.ForeignKey(Truck, null=True, on_delete=models.CASCADE)


class DispatcherProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="dispatcher_profile", on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=255)


class Broker(models.Model):  # TODO add more details (broker MC)
    agent_name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.company_name}"


generate_load_id = partial(
    generate_model_custom_id, model_name="BookedLoad", custom_id_field_name="load_id", default_value=2000
)

generate_invoice_id = partial(
    generate_model_custom_id, model_name="BookedLoad", custom_id_field_name="invoice_id", default_value=330000
)


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
    supported_truck_kind = models.ManyToManyField(Truck)
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


class Billing(BookedLoad):
    class Meta:
        proxy = True
        verbose_name_plural = "Billing"
