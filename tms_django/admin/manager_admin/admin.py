from apps.tms.models import (
    Billing,
    BookedLoad,
    Broker,
    DispatcherProfile,
    DriverProfile,
    Truck,
)
from apps.users.models import User
from django.contrib import admin
from django.contrib.admin import AdminSite


class ManagerAdminSite(AdminSite):
    site_header = "Transportation Management System"
    site_title = "Manager Page"
    index_title = "Welcome to the Manager View"


manager_admin = "manager_admin"

manager_admin_site = ManagerAdminSite(name=manager_admin)
