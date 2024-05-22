import unittest.mock

from api.v1.serializers import DriverProfileListSerializer, MilesCountSerializer
from apps.tms.models import DriverProfile, Truck, TruckKind
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class DriverProfileAPITestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        """
        Will be called once for all tests in this class;
        Will be called *before* all tests;
        """
        super().setUpClass()
        cls.admin = User.objects.create_user(username="admin", is_staff=True, is_superuser=True)
        ...

    @classmethod
    def tearDownClass(cls):
        """
        Will be called once, for all tests in this class;
        Will be called *after* all tests are completed;
        """
        super().tearDownClass()
        ...

    def setUp(self) -> None:
        """
        Will be called before every test in this class;
        """
        # 1. Preparing data and context needed for this test
        self.driver_user = User.objects.create_user(username="test", first_name="Vasya", last_name="Pupkin")
        self.driver_profile = DriverProfile.objects.create(user=self.driver_user)

    def tearDown(self):
        """
        Will be called after every test in this class;
        """
        ...

    def test_serializer__get_full_name(self):
        expected_result = f"{self.driver_user.first_name} {self.driver_user.last_name}"
        result = DriverProfileListSerializer.get_full_name(obj=self.driver_profile)
        self.assertEqual(result, expected_result)

    def test_driverprofile_list__no_driver_profiles(self):
        # 2. Removing DriverProfile record (created in setUp method)
        self.driver_profile.delete()
        # 3. Triggering request
        url = reverse("api:v1:driverprofile-list")
        response = self.client.get(url, format="json")
        # 3. Making sure all in check
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)
        self.assertEqual(response.data["results"], [])

    def test_driverprofile_list(self):
        # 2. Triggering request
        url = reverse("api:v1:driverprofile-list")
        response = self.client.get(url, format="json")
        # 3. Making sure we received what we hope to
        self.driver_profile.refresh_from_db()  # <- updating python instance with database record state
        self.driver_user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertIsNotNone(response.json()["results"][0]["full_name"])
        self.assertIsNotNone(response.json()["results"][0]["id"])
        self.assertEqual(response.json()["results"][0]["id"], self.driver_profile.id)

    def test_driverprofile_detail(self):
        url = reverse("api:v1:driverprofile-detail", kwargs={"pk": self.driver_profile.id})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["user"]["username"], self.driver_profile.user.username)

    def test_driverprofile_delete(self):
        url = reverse("api:v1:driverprofile-detail", kwargs={"pk": self.driver_profile.id})
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(DriverProfile.objects.filter(id=self.driver_profile.id).exists(), False)
        self.assertEqual(User.objects.filter(id=self.driver_profile.user.id).exists(), True)

    def test_driverprofile_update__validation(self):
        url = reverse("api:v1:driverprofile-detail", kwargs={"pk": self.driver_profile.id})
        # first_name validation:
        first_name_before_update = str(self.driver_user.first_name)
        request_data = {"user": {"first_name": "123"}}
        response = self.client.put(url, request_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.json()["user"]["first_name"]), 1)
        self.assertIn("Do not use digits!", response.json()["user"]["first_name"][0])
        self.driver_profile.refresh_from_db()
        self.driver_user.refresh_from_db()
        self.assertEqual(self.driver_user.first_name, first_name_before_update)

    def test_driverprofile_update(self):
        url = reverse("api:v1:driverprofile-detail", kwargs={"pk": self.driver_profile.id})
        request_data = {
            "user": {"first_name": "Tolik", "last_name": "Tree", "email": "tolik@gmail.com"},
            "phone_number": "77778862",
            "driver_licence": "KD85962",
            "address": "2112 Ditmas Ave, Brooklyn, NY",
        }

        response = self.client.put(url, data=request_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["user"]["first_name"], "Tolik")

    def test_driverprofile_create(self):
        # self.driver_profile.create()
        truck_small_st = Truck.objects.create(kind=TruckKind.SMALL_STRAIGHT, weight=5000, capacity=2000)
        truck_sprinter = Truck.objects.create(kind=TruckKind.SPRINTER, weight=5000, capacity=2000)
        url = reverse("api:v1:driverprofile-list")
        request_data = {
            "truck": truck_sprinter.id,
            "user": {"first_name": "Elya", "last_name": "Smith", "email": "elya.smith@gmail.com"},
            "phone_number": "9924782153",
            "driver_licence": "MC46579",
            "address": "2152 Bakery St, Columbus, OH",
        }

        self.assertEqual(DriverProfile.objects.count(), 1)

        response = self.client.post(url, data=request_data, format="json")

        print(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DriverProfile.objects.count(), 2)
        new_driver_profile = DriverProfile.objects.get(id=response.json()["id"])
        self.assertEqual(new_driver_profile.truck.id, truck_sprinter.id)


class MilesCountApiTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.zipcodeapi_200 = 200, {"distance": 100}
        cls.zipcodeapi_404 = 404, {"error_code": 404, "error_msg": 'Zip code "90110" not found.'}
        cls.zipcodeapi_401 = 401, {"error_code": 401, "error_msg": "Application is not authorized."}

    def test_count_miles_api_request(self):
        url = reverse("api:v1:count_miles")
        request_data = {"pickup_zip_code": 19116, "delivery_zip_code": 90210}
        response = self.client.post(url, data=request_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())

    def test_count_miles_api_request__mock(self):
        # 1. 200 response scenario:
        with unittest.mock.patch.object(
            MilesCountSerializer,
            "_zipcode_api_request",
            return_value=self.zipcodeapi_200,
        ) as mock_zipcode_api_request:
            url = reverse("api:v1:count_miles")
            request_data = {"pickup_zip_code": 19116, "delivery_zip_code": 90210}
            response = self.client.post(url, data=request_data, format="json")
            self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
