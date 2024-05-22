import apps
from admin.manager_admin.admin import manager_admin_site
from admin.super_admin.admin import admin
from apps import tms
from django.urls import include, path

urlpatterns = [
    # Admin
    path("admin_super/", admin.site.urls),
    path("admin_manager/", manager_admin_site.urls),
    # API
    path("api/", include("api.urls")),
    path("api/auth/", include("rest_framework.urls", namespace="rest_framework")),
    # APP
    path("tms/", include("apps.tms.urls")),
]
