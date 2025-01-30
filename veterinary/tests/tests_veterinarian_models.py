from model_bakery import baker
from django.test import TestCase
from datetime import date

from ..models import Veterinarian


class VeterinarianTest(TestCase):
    """Veterinarian Model"""

    def setUp(self):
        self.user = baker.make("account.User", phone="09151498722")

        self.payload = {
            "license_image": "license.png",
            "national_id_image": "national.jpeg",
            "medical_license": "09338973928",
            "issuance_date": date.today(),
        }
        self.model = Veterinarian.objects.create(user=self.user, **self.payload)

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
