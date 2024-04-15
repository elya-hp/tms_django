from admin.manager_admin.admin import manager_admin_site
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    path("manager_admin/", manager_admin_site.urls),
    # API
    path("api/", include("api.urls")),
    path("api/auth/", include("rest_framework.urls", namespace="rest_framework")),
]
