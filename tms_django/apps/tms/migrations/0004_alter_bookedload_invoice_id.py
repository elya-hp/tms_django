# Generated by Django 5.0.4 on 2024-04-30 17:35

import apps.tms.generators
import functools
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tms', '0003_remove_bookedload_supported_truck_kind'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookedload',
            name='invoice_id',
            field=models.CharField(db_index=True, default=functools.partial(apps.tms.generators.generate_model_custom_id, *(), **{'custom_id_field_name': 'invoice_id', 'default_value': 330000, 'model_name': 'BookedLoad'}), max_length=8, unique=True),
        ),
    ]
