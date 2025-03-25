from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from model_bakery import baker
from ..models import Veterinarian

VETERINARIAN_SEARCH_URL = reverse("veterinary:search_veterinarian")


class VeterinarianSearchTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.province_1 = baker.make("province.Province", name="province 1")
        self.city_1 = baker.make("province.City", province=self.province_1)

        self.province_2 = baker.make("province.Province", name="province 2")
        self.city_2 = baker.make("province.City", province=self.province_2)

        self.user_1 = baker.make(
            "account.User", phone="09151498722", fullName="Hamid Balalzadeh"
        )
        self.user_2 = baker.make(
            "account.User", phone="09151498723", fullName="Khosro Rasuli"
        )
        self.user_3 = baker.make(
            "account.User", phone="09151498724", fullName="Ali Riki"
        )
        self.user_4 = baker.make(
            "account.User", phone="09151498725", fullName="Iman Samani"
        )

        self.veterinarian_1 = baker.make(
            Veterinarian,
            user=self.user_1,
            province=self.province_1,
            city=self.city_1,
            state="C",
        )
        self.veterinarian_2 = baker.make(
            Veterinarian,
            user=self.user_2,
            province=self.province_1,
            city=self.city_1,
            state="C",
        )
        self.veterinarian_3 = baker.make(
            Veterinarian,
            user=self.user_3,
            province=self.province_2,
            city=self.city_2,
            state="C",
        )
        self.veterinarian_4 = baker.make(
            Veterinarian,
            user=self.user_4,
            province=self.province_1,
            city=self.city_1,
            state="P",
        )

    def test_search_by_fullName(self):
        url = VETERINARIAN_SEARCH_URL
        response = self.client.get(url, {"fullName": "Hamid"})
        res_json_res = response.json()["results"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_json_res), 1)  # Only one product matches

    def test_search_by_province(self):
        url = VETERINARIAN_SEARCH_URL
        response = self.client.get(url, {"province": self.province_1.id})
        res_json_res = response.json()["results"]

        len_veters = (
            Veterinarian.objects.get_confirmed_veters()
            .filter(
                province__id=self.province_1.id,
            )
            .count()
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_json_res), len_veters)  # Only one product matches

    def test_search_by_city(self):
        url = VETERINARIAN_SEARCH_URL
        response = self.client.get(url, {"city": self.city_1.id})
        res_json_res = response.json()["results"]

        len_veters = (
            Veterinarian.objects.get_confirmed_veters()
            .filter(city__id=self.city_1.id)
            .count()
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_json_res), len_veters)  # Only one product matches
