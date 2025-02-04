from model_bakery import baker
from django.test import TestCase
from datetime import date

from ..models import Veterinarian, MedicalCenter


class VeterinarianTest(TestCase):
    """Veterinarian Model Test"""

    def setUp(self):
        self.user = baker.make("account.User", phone="09151498722")
        self.province = baker.make("province.Province")
        self.city = baker.make("province.City", province=self.province)

        self.payload = {
            "clinic_name": "test clinic",
            "license_image": "license.png",
            "national_id_image": "national.jpeg",
            "medical_license": "09338973928",
            "issuance_date": date.today(),
        }
        self.model = Veterinarian.objects.create(
            user=self.user, province=self.province, city=self.city, **self.payload
        )

    def test_create_model_should_work_properly(self):
        """Test create model"""
        for k, v in self.payload.items():
            self.assertEqual(getattr(self.model, k), v)

        self.assertEqual(self.model.user, self.user)

    def test_str_obj_should_work_properly(self):
        """test str"""
        self.assertEqual(
            str(self.model),
            f"{self.payload.get('medical_license', 'test')} - {self.user.phone}",
        )


class MedicalCenterTest(TestCase):
    """Medical Center Model Test"""

    def setUp(self):
        self.gallery = baker.make("gallery.Gallery")

        self.payload = {"title": "test", "description": "test desc"}
        self.model = MedicalCenter.objects.create(gallery=self.gallery, **self.payload)

    def test_create_model_should_work_properly(self):
        """Test create model"""
        for k, v in self.payload.items():
            self.assertEqual(getattr(self.model, k), v)

        self.assertEqual(self.model.gallery, self.gallery)

    def test_str_obj_should_work_properly(self):
        """test str"""
        self.assertEqual(
            str(self.model),
            self.payload.get("title", "test"),
        )
