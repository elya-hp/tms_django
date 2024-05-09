from apps.tms.models import (
    Billing,
    BookedLoad,
    Broker,
    DispatcherProfile,
    DriverProfile,
    Truck,
)
from django.contrib import admin
from django.contrib.auth import get_user_model

admin.site.site_header = "Super-Admin Transportation Management System"


User = get_user_model()


@admin.register(Broker)
class BrokerAdmin(admin.ModelAdmin):
    list_display = (
        "company_name",
        "agent_name",
        "mc_number",
    )


@admin.register(Truck)
class TruckAdmin(admin.ModelAdmin):
    list_display = (
        "kind",
        "weight",
        "capacity",
    )


@admin.register(BookedLoad)
class BookedLoadAdmin(admin.ModelAdmin):
    list_display = ["load_id", "status", "broker", "pickup_location", "delivery_location", "driver"]
    list_filter = ["load_id", "status", "driver", "dispatcher", "broker"]
    search_fields = (
        "load_id",
        "driver__unit_id",
        "driver__first_name",
        "driver__last_name",
        "dispatcher__first_name",
        "dispatcher__last_name",
        "broker__company_name",
    )
    readonly_fields = ("pk", "load_id")

    fields = (
        "load_id",
        "status",
        "driver",
        "pickup_location",
        "delivery_location",
        "distance",
        "pallets_quantity",
        "pallets_weight",
        "dispatcher",
        "broker",
        "total_rate",
        "driver_rate",
    )


@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    fields = (
        "load_id",
        "broker",
        "status",
        "pickup_location",
        "delivery_location",
        "total_rate",
    )

    list_display = [
        "load_id",
        "broker",
        "status",
        "pickup_location",
        "delivery_location",
        "total_rate",
    ]

    Status = {
        "INVOICED": "invoiced",
    }

    actions = ("mark_loads_as_invoiced",)

    def get_queryset(self, request):
        qs = (
            super()
            .get_queryset(request)
            .filter(
                status__in=[
                    Billing.Status.DELIVERED,
                    Billing.Status.CANCELLED,
                ]
            )
        )

        return qs

    def mark_loads_as_invoiced(self, request, queryset):
        queryset.update(status="invoiced")
