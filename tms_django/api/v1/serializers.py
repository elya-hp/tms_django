import os
import uuid

import httpx
from apps.tms.models import DispatcherProfile, DriverProfile
from django.contrib.auth import get_user_model
from rest_framework import serializers, status
from rest_framework.exceptions import APIException, ValidationError

User = get_user_model()


class NestedUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
        )

    def validate_first_name(self, first_name: str) -> str:
        if any([letter.isdigit() for letter in first_name]):
            raise ValidationError(f"Do not use digits! ({first_name})")
        return first_name


class DriverProfileSerializer(serializers.ModelSerializer):
    user = NestedUserSerializer()
    unit_id = serializers.CharField(read_only=True)

    class Meta:
        model = DriverProfile
        fields = "__all__"

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        # 1. Create User
        user_data = validated_data.pop("user")
        user_data["username"] = uuid.uuid4().hex
        user = self.fields["user"].create(user_data)

        # 2. Create DriverProfile with a link to the User record
        validated_data["user"] = user
        driver_profile = super().create(validated_data)
        return driver_profile

    def update(self, instance: DriverProfile, validated_data):
        # Update User data if provided
        user_validated_data = validated_data.pop("user", None)
        if user_validated_data:
            self.fields["user"].update(instance.user, user_validated_data)

        return super().update(instance, validated_data)


class DispatcherProfileSerializer(serializers.ModelSerializer):
    user = NestedUserSerializer()

    class Meta:
        model = DispatcherProfile
        fields = "__all__"

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        # 1. Create User
        user_data = validated_data.pop("user")
        user_data["username"] = uuid.uuid4().hex
        user = self.fields["user"].create(user_data)

        # 2. Create DispatcherProfile with a link to the User record
        validated_data["user"] = user
        dispatcher_profile = super().create(validated_data)
        return dispatcher_profile

    def update(self, instance: DispatcherProfile, validated_data):
        # Update User data if provided
        user_validated_data = validated_data.pop("user", None)
        if user_validated_data:
            self.fields["user"].update(instance.user, user_validated_data)

        return super().update(instance, validated_data)


class DriverProfileListSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = DriverProfile
        fields = [
            "id",
            "user",
            "unit_id",
            "full_name",
        ]

    @classmethod
    def get_full_name(cls, obj: DriverProfile) -> str:
        return f"{obj.user.first_name} {obj.user.last_name}"


class DispatcherProfileListSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = DispatcherProfile
        fields = "__all__"

    @classmethod
    def get_full_name(cls, obj: DispatcherProfile) -> str:
        return f"{obj.user.first_name} {obj.user.last_name}"


class MilesCountSerializer(serializers.Serializer):
    pickup_zip_code = serializers.IntegerField()
    delivery_zip_code = serializers.IntegerField()
    miles_count = serializers.IntegerField(read_only=True)

    @classmethod
    def format_zip_code(cls, value):
        return value

    @staticmethod
    def _zipcode_api_request(endpoint: str) -> tuple[int, dict]:
        # TODO: move to environment variable
        api_key = os.getenv("API_KEY")
        api_url = f"https://www.zipcodeapi.com/rest/{api_key}/{endpoint}"
        headers = {"Content-Type": "application/json"}
        response = httpx.get(api_url, headers=headers)
        return response.status_code, response.json()

    @classmethod
    def count_miles_api_request(cls, zip_from, zip_to):
        units = "mile"
        endpoint = f"distance.json/{zip_from}/{zip_to}/{units}"
        status_code, response_data = cls._zipcode_api_request(endpoint=endpoint)
        if status_code == 200:
            return response_data.get("distance", 0)

        elif status_code == 401:
            raise APIException(
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"zipcodeapi responded with error: {response_data}",
            )

        elif status_code == 404:
            raise ValidationError(
                detail=f"zipcodeapi responded with error: {response_data}",
            )
        else:
            raise APIException(detail=f"something went wrong, error code: {response_data}")

    @classmethod
    def count_miles(cls, pickup_zip_code: int, delivery_zip_code: int) -> int:
        zip_from = cls.format_zip_code(pickup_zip_code)
        zip_to = cls.format_zip_code(delivery_zip_code)
        miles_count = cls.count_miles_api_request(zip_from, zip_to)
        return miles_count
