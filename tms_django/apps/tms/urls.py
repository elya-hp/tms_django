from apps.tms import views
from django.urls import path

app_name = "tms"

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home_page"),
    path("load/", views.BookedLoadCreateView.as_view(), name="load_create"),
    path("load/<int:pk>/", views.BookedLoadDetailView.as_view(), name="load_detail"),
    path("load/<int:pk>/update/", views.BookedLoadUpdateView.as_view(), name="load_update"),
    path("load/<int:pk>/delete/", views.BookedLoadDeleteView.as_view(), name="load_delete"),
    path("load/list/", views.booked_load_filtered, name="loadlist"),
]
