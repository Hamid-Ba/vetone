import os
from django.test import TestCase

from django.urls import reverse
from rest_framework.test import APIClient
from datetime import date
from rest_framework import status
from model_bakery import baker

from province.models import Address

from ..models import Veterinarian, Rancher, Animal
from ..serializers import AnimalSerializer

MEDICAL_CENTER_URL = reverse("veterinary:centers")
LIST_ANIMAL_URL = reverse("veterinary:animals")
ADD_RANCHER_URL = reverse("veterinary:add_rancher")
REGISTER_VETERINARIAN_URL = reverse("veterinary:register_veterinarian")


def remove_rancher_url(phone: str):
    return reverse("veterinary:remove_rancher", kwargs={"phone": phone})


class PrivateTest(TestCase):
    """Test Those Endpoints Who Need User To Be Authorized"""

    def setUp(self):
        self.client = APIClient()
        self.user = baker.make("account.User", phone="09151498722")
        self.client.force_authenticate(self.user)

    def test_get_list_of_animals_list(self):
        """Test Get List Of Animals List"""
        animal_1 = baker.make(Animal)
        animal_2 = baker.make(Animal)

        res = self.client.get(LIST_ANIMAL_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        animal_1 = AnimalSerializer(animal_1, many=False).data
        animal_2 = AnimalSerializer(animal_2, many=False).data

        self.assertIn(animal_1, res.json())
        self.assertIn(animal_2, res.json())
