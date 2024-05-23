from functools import partial

from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.db import OperationalError
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


generate_unit_id = partial(
    generate_model_custom_id, model_name="DriverProfile", custom_id_field_name="unit_id", default_value=1000
)

generate_load_id = partial(
    generate_model_custom_id, model_name="BookedLoad", custom_id_field_name="load_id", default_value=2000
)

generate_invoice_id = partial(
    generate_model_custom_id, model_name="BookedLoad", custom_id_field_name="invoice_id", default_value=330000
)
