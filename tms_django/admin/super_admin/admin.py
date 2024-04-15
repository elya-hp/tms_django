from django.contrib import admin
from django.contrib.auth import get_user_model

admin.site.site_header = "Transportation Management System"


User = get_user_model()
