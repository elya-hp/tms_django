from api.v1 import serializers
from api.v1.serializers import MilesCountSerializer
from apps.tms.models import DispatcherProfile, DriverProfile
from rest_framework import permissions, views, viewsets
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.serializers import Serializer


class IsAdminOrDriverOwner(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_object_permission(self, request, view, obj: DriverProfile):
        driver_profile: DriverProfile = obj

        if request.user.is_superuser:
            return True

        request_user_is_driver_profile_owner: bool = driver_profile.user == request.user
        if request_user_is_driver_profile_owner:
            return True

        return False


class IsAdminOrDispatcherOwner(BasePermission):
    def has_object_permission(self, request, view, obj: DispatcherProfile):
        dispatcher_profile: DispatcherProfile = obj

        if request.user.is_superuser:
            return True

        request_user_is_dispatcher_profile_owner: bool = dispatcher_profile.user == request.user
        if request_user_is_dispatcher_profile_owner:
            return True

        return False


class DriverProfileViewSet(viewsets.ModelViewSet):
    queryset = DriverProfile.objects.all().order_by("unit_id")
    serializer_class_map: dict[str, Serializer] = {
        "list": serializers.DriverProfileListSerializer,
    }
    default_serializer_class = serializers.DriverProfileSerializer
    # permission_classes = [permissions.IsAuthenticated, IsAdminOrDriverOwner]

    def get_serializer_class(self):
        return self.serializer_class_map.get(self.action, self.default_serializer_class)


class DispatcherProfileViewSet(viewsets.ModelViewSet):
    queryset = DispatcherProfile.objects.all()
    serializer_class_map: dict[str, Serializer] = {
        "list": serializers.DispatcherProfileListSerializer,
    }
    default_serializer_class = serializers.DispatcherProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrDispatcherOwner]

    def get_serializer_class(self):
        return self.serializer_class_map.get(self.action, self.default_serializer_class)


class MilesCountViewSet(views.APIView):
    serializers_class = MilesCountSerializer

    def post(self, request):
        serializer = self.serializers_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        miles_count = serializer.count_miles(**serializer.validated_data)
        return Response(status=200, data={"miles_count": miles_count})
