from model_bakery import baker
from django.test import TestCase
from datetime import date

from ..models import Rancher


class RancherTest(TestCase):
    """Rancher Model Test"""

    def setUp(self):
        self.user = baker.make("account.User", phone="09151498722", fullName="Hamid Balalzadeh")
        self.province = baker.make("province.Province")
        self.city = baker.make("province.City", province=self.province)

        self.model = Rancher.objects.create(
            user=self.user,
            province=self.province,
            city=self.city,
        )

    def test_create_model_should_work_properly(self):
        """Test create model"""
        self.assertEqual(self.model.user, self.user)
        self.assertEqual(self.model.city, self.city)
        self.assertEqual(self.model.province, self.province)

    def test_str_obj_should_work_properly(self):
        """test str"""
        self.assertEqual(
            str(self.model),
            f"{self.user.fullName} - {self.user.phone}",
        )
