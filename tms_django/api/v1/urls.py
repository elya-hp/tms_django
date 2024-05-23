from api.v1 import views
from django.urls import include, path
from rest_framework import routers

app_name = "v1"
router = routers.DefaultRouter()

router.register(r"driver", views.DriverProfileViewSet)
router.register(r"dispatcher", views.DispatcherProfileViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("count_miles/", views.MilesCountViewSet.as_view(), name="count_miles"),
]
