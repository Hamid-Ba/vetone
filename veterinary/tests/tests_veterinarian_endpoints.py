import os
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from django.urls import reverse
from rest_framework.test import APIClient
from datetime import date
from rest_framework import status
from model_bakery import baker
from io import BytesIO
from PIL import Image

from province.models import Address

from ..models import Veterinarian, MedicalCenter, Rancher
from ..serializers import MedicalCenterSerializer, RancherVeterinarianSerializer

MEDICAL_CENTER_URL = reverse("veterinary:centers")
LIST_RANCHER_URL = reverse("veterinary:ranchers")
ADD_RANCHER_URL = reverse("veterinary:add_rancher")
REGISTER_VETERINARIAN_URL = reverse("veterinary:register_veterinarian")


def remove_rancher_url(phone: str):
    return reverse("veterinary:remove_rancher", kwargs={"phone": phone})


class PublicTest(TestCase):
    """Test Those Endpoints Who Do Not Need User To Be Authorized"""

    def setUp(self):
        self.client = APIClient()

    def test_medical_center_list_api_should_work_properly(self):
        """Test Medical Center List API"""

        center_1 = baker.make(MedicalCenter)
        center_2 = baker.make(MedicalCenter)

        res = self.client.get(MEDICAL_CENTER_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertIn(MedicalCenterSerializer(center_1).data, res.json())
        self.assertIn(MedicalCenterSerializer(center_2).data, res.json())


class PrivateTest(TestCase):
    """Test Those Endpoints Who Need User To Be Authorized"""

    def setUp(self):
        self.client = APIClient()
        self.user = baker.make("account.User", phone="09151498722")
        self.client.force_authenticate(self.user)
        self.medical_center = baker.make(MedicalCenter)
        self.uploaded_files = []  # Store file paths for cleanup

    def _generate_test_image(self):
        """Generate a valid in-memory image file."""
        img = Image.new("RGB", (100, 100), color=(255, 0, 0))  # Create a red image
        img_io = BytesIO()
        img.save(img_io, format="JPEG")
        img_io.seek(0)
        return SimpleUploadedFile(
            "test_image.jpg", img_io.getvalue(), content_type="image/jpeg"
        )

    def test_register_veterinarian_request(self):
        """Test Register Veterinarian"""
        license_image = self._generate_test_image()
        national_id_image = self._generate_test_image()
        payload = {
            "license_image": license_image,
            "national_id_image": national_id_image,
            "medical_license": "09338973928",
            "issuance_date": date.today(),
            "medical_center": self.medical_center.id,
            "street": "test",
            "clinic_name": "test",
            "latitude": "2",
            "longitude": "1",
            "fullName": "test",
            "image": self._generate_test_image(),
        }

        self.assertTrue(Rancher.objects.filter(user=self.user).exists())

        res = self.client.post(REGISTER_VETERINARIAN_URL, payload, format="multipart")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        veter = Veterinarian.objects.first()
        veter_address = Address.objects.get(user=veter.user)

        self.assertEqual(veter.user, self.user)
        self.assertFalse(Rancher.objects.filter(user=self.user).exists())
        self.assertEqual(veter_address.street, payload["street"])
        self.assertEqual(veter_address.clinic_name, payload["clinic_name"])
        self.assertEqual(veter_address.latitude, payload["latitude"])
        self.assertEqual(veter_address.longitude, payload["longitude"])

        if veter.license_image:
            self.uploaded_files.append(veter.license_image.path)
        if veter.national_id_image:
            self.uploaded_files.append(veter.national_id_image.path)

    def test_add_rancher_should_work_properly(self):
        """Test Add Rancher"""
        baker.make(Veterinarian, user=self.user, state="C")

        payload = {
            "fullName": "test",
            "phone": "09151498721",
            "latitude": "2",
            "longitude": "1",
        }

        res = self.client.post(ADD_RANCHER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        rancher = Rancher.objects.get(user__phone=payload["phone"])
        rancher_address = Address.objects.get(user=rancher.user)

        self.assertEqual(rancher.user.fullName, payload["fullName"])
        self.assertEqual(rancher.veterinarians.first().user, self.user)

        self.assertEqual(rancher_address.latitude, payload["latitude"])
        self.assertEqual(rancher_address.longitude, payload["longitude"])

    def test_get_list_of_veterinarian_ranchers_api(self):
        """Test Get List Of Veterinarian Rancher"""
        veteinarian = baker.make(Veterinarian, user=self.user)

        user_1 = baker.make("account.User", phone="09151498723")
        veteinarian_2 = baker.make(Veterinarian, user=user_1)

        user_2 = baker.make("account.User", phone="09151498721")
        rancher_1 = Rancher.objects.get(user=user_2)
        rancher_1.veterinarians.add(veteinarian)

        user_3 = baker.make("account.User", phone="09151498720")
        rancher_2 = Rancher.objects.get(user=user_3)
        rancher_2.veterinarians.add(veteinarian)
        rancher_2.veterinarians.add(veteinarian_2)

        res = self.client.get(LIST_RANCHER_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        rancher_1 = RancherVeterinarianSerializer(rancher_1, many=False).data
        rancher_2 = RancherVeterinarianSerializer(rancher_2, many=False).data

        self.assertIn(rancher_1, res.json()["results"])
        self.assertIn(rancher_2, res.json()["results"])

    def test_delete_rancher_from_veterinarian_list_api(self):
        """Test Delete Rancher From Veterinarian List"""
        veteinarian = baker.make(Veterinarian, user=self.user)

        user_2 = baker.make("account.User", phone="09151498721")
        rancher = Rancher.objects.get(user=user_2)
        rancher.veterinarians.add(veteinarian)

        self.assertTrue(rancher.veterinarians.contains(veteinarian))

        url = remove_rancher_url(user_2.phone)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        rancher.refresh_from_db()

        self.assertFalse(rancher.veterinarians.contains(veteinarian))

    def tearDown(self):
        """Clean up test images after the test"""
        for file_path in self.uploaded_files:
            if os.path.exists(file_path):
                os.remove(file_path)
