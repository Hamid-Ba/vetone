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

from ..models import Veterinarian, MedicalCenter

REGISTER_VETERINARIAN_URL = reverse("veterinary:register_veterinarian")


class PrivateTest(TestCase):
    """Test Those Endpoints Which Need User To Be Authorized"""

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
        }

        res = self.client.post(REGISTER_VETERINARIAN_URL, payload, format="multipart")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        veter = Veterinarian.objects.first()

        self.assertEqual(veter.user, self.user)

        if veter.license_image:
            self.uploaded_files.append(veter.license_image.path)
        if veter.national_id_image:
            self.uploaded_files.append(veter.national_id_image.path)

    def tearDown(self):
        """Clean up test images after the test"""
        for file_path in self.uploaded_files:
            if os.path.exists(file_path):
                os.remove(file_path)
