from model_bakery import baker
from django.test import TestCase

from ..models import Rancher, Animal


class RancherTest(TestCase):
    """Rancher Model Test"""

    def setUp(self):
        self.user = baker.make(
            "account.User", phone="09151498722", fullName="Hamid Balalzadeh"
        )

        self.model = Rancher.objects.get(user=self.user)

    def test_create_model_should_work_properly(self):
        """Test create model"""
        self.assertEqual(self.model.user, self.user)

    def test_str_obj_should_work_properly(self):
        """test str"""
        self.assertEqual(
            str(self.model),
            f"{self.user.fullName} - {self.user.phone}",
        )


class AnimalTest(TestCase):
    """Aniaml Model Test"""

    def setUp(self):
        self.payload = {"name": "test"}

        self.image = baker.make("gallery.Gallery")

        self.model = Animal.objects.create(image=self.image, **self.payload)

    def test_create_model_should_work_properly(self):
        """Test create model"""
        for k, v in self.payload.items():
            self.assertEqual(getattr(self.model, k), v)
        self.assertEqual(self.model.image, self.image)

    def test_str_obj_should_work_properly(self):
        """test str"""
        self.assertEqual(
            str(self.model),
            f"{self.payload['name']}",
        )
