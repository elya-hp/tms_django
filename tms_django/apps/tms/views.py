import django_filters
from django.forms import ModelForm
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .models import BookedLoad


class HomePageView(TemplateView):
    template_name = "home_page.html"


class BookedLoadCreateForm(ModelForm):
    class Meta:
        model = BookedLoad
        fields = [
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
        ]


class BookedLoadCreateView(CreateView):
    model = BookedLoad
    form_class = BookedLoadCreateForm
    template_name = "bookedload_create_form.html"

    def get_success_url(self):
        return reverse("tms:load_detail", kwargs={"pk": self.object.pk})


#
class BookedLoadDetailView(DetailView):
    model = BookedLoad
    template_name = "bookedload_detail.html"


class BookedLoadListView(ListView):
    model = BookedLoad
    template_name = "bookedload_list.html"
    context_object_name = "load_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        load_list = list(self.get_queryset().values())
        context["load_list"] = load_list
        return context


class BookedLoadUpdateView(UpdateView):
    model = BookedLoad
    fields = "__all__"
    template_name = "bookedload_update_form.html"
    success_url = reverse_lazy("tms:load_list")


class BookedLoadDeleteView(DeleteView):
    model = BookedLoad
    success_url = reverse_lazy("tms:load_list")


class BookedLoadFilter(django_filters.FilterSet):
    class Meta:
        model = BookedLoad
        fields = ["load_id", "status", "dispatcher", "broker"]


def booked_load_filtered(request):
    f = BookedLoadFilter(request.GET, queryset=BookedLoad.objects.all())
    return render(request, "bookedload_list.html", {"filter": f})
