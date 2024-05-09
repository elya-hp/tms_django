from apps.tms.models import (
    Billing,
    BookedLoad,
    Broker,
    DispatcherProfile,
    DriverProfile,
    Truck,
)
from apps.users.models import DispatcherUser, DriverUser, User
from django.contrib import admin
from django.contrib.admin import AdminSite


class ManagerAdminSite(AdminSite):
    site_header = "Transportation Management System"
    site_title = "Manager Page"
    index_title = "Welcome to the Manager View"


manager_admin = "manager_admin"
manager_admin_site = ManagerAdminSite(name=manager_admin)


@admin.register(Billing, BookedLoad, Broker, Truck, site=manager_admin_site)
class ManagerUserAdmin(admin.ModelAdmin):
    ...


class DispatcherProfileInLine(admin.StackedInline):
    model = DispatcherProfile

    def has_delete_permission(self, request, obj=None):
        return False


class DriverProfileInLine(admin.StackedInline):
    model = DriverProfile
    readonly_fields = ["unit_id"]

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(DispatcherUser, site=manager_admin_site)
class DispatcherUserAdmin(admin.ModelAdmin):
    list_filter = ("user_type",)
    search_fields = (
        "first_name",
        "last_name",
    )
    list_display = (
        "id",
        "first_name",
        "last_name",
        "user_type",
    )
    inlines = [
        DispatcherProfileInLine,
    ]
    fields = (
        "first_name",
        "last_name",
        "user_type",
        "username",
    )
    list_display_links = (
        "id",
        "first_name",
        "last_name",
    )
    readonly_fields = ("user_type",)

    def get_form(self, request, obj=None, **kwargs):
        form = super(DispatcherUserAdmin, self).get_form(request, obj, **kwargs)
        return form

    def save_model(self, request, obj, form, change):
        obj.user_type = User.UserType.DISPATCHER
        super().save_model(request, obj, form, change)


@admin.register(DriverUser, site=manager_admin_site)
class DriverUserAdmin(admin.ModelAdmin):
    list_filter = ("user_type",)
    list_select_related = ("driver_profile",)
    search_fields = (
        # "unit_id",
        "first_name",
        "last_name",
    )
    list_display = (
        # "unit_id",
        "first_name",
        "last_name",
        "user_type",
        # "truck",
    )

    inlines = [
        DriverProfileInLine,
    ]

    fields = (
        "first_name",
        "last_name",
        "user_type",
        "username",
    )

    readonly_fields = ("user_type",)

    @admin.display()
    def unit_id(self) -> str:
        return self.driver_profile.unit_id

    @admin.display()
    def truck(self) -> str:
        return self.driver_profile.truck

    def get_form(self, request, obj=None, **kwargs):
        form = super(DriverUserAdmin, self).get_form(request, obj, **kwargs)
        return form

    def save_model(self, request, obj, form, change):
        obj.user_type = User.UserType.DRIVER
        super().save_model(request, obj, form, change)
