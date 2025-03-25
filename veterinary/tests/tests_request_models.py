from datetime import date, time
from model_bakery import baker
from django.test import TestCase

from ..models import Request, AnimalRequest, Rancher, Animal, Veterinarian


class RequestTest(TestCase):
    """Request Model Test"""

    def setUp(self):
        self.rancher_user = baker.make(
            "account.User", phone="09151498722", fullName="Hamid Balalzadeh"
        )
        self.rancher = Rancher.objects.get(user=self.rancher_user)

        self.veterinarian_user = baker.make("account.User", phone="09151498721")
        self.veterinary = baker.make(Veterinarian, user=self.veterinarian_user)

        self.payload = {
            # Make This a model
            # "animal": self.animal.id,
            # "animal_count": 1,
            # "animal_weight": 45,
            # "animal_sign": "test",
            "description": "test",
            "voice": "voice.mp3",
            "video": "video.mp4",
            "type": 1,
            "date": date.today(),
            "time": time(17, 35),
        }

        self.model = Request.objects.create(
            veterinarian=self.veterinary, rancher=self.rancher, **self.payload
        )

    def test_create_model_should_work_properly(self):
        """Test create model"""
        for k, v in self.payload.items():
            self.assertEqual(getattr(self.model, k), v)

        self.assertEqual(self.model.veterinarian, self.veterinary)
        self.assertEqual(self.model.rancher, self.rancher)

    def test_str_obj_should_work_properly(self):
        """test str"""
        self.assertEqual(
            str(self.model),
            f"Rancher: {self.rancher.user.phone} - Veteinarian: {self.veterinary.user.phone} - {self.model.created_at}",
        )


class AnimalRequestTest(TestCase):
    """Aniaml Request Model Test"""

    def setUp(self):
        self.rancher_user = baker.make(
            "account.User", phone="09151498722", fullName="Hamid Balalzadeh"
        )
        self.rancher = Rancher.objects.get(user=self.rancher_user)

        self.veterinarian_user = baker.make("account.User", phone="09151498721")
        self.veterinary = baker.make(Veterinarian, user=self.veterinarian_user)

        self.request = baker.make(
            Request, rancher=self.rancher, veterinarian=self.veterinary
        )

        self.animal = baker.make(Animal)

        self.payload = {
            "count": 1,
            "weight": 45,
            "sign": "test",
        }

        self.model = AnimalRequest.objects.create(
            request=self.request, animal=self.animal, **self.payload
        )

    def test_create_model_should_work_properly(self):
        """Test create model"""
        for k, v in self.payload.items():
            self.assertEqual(getattr(self.model, k), v)

        self.assertEqual(self.model.request, self.request)
        self.assertEqual(self.model.animal, self.animal)

    def test_str_obj_should_work_properly(self):
        """test str"""
        self.assertEqual(
            str(self.model),
            f"Request ID: {self.request.id} - {self.animal}",
        )


# class RequestImageTest(TestCase):
#     """Request Image Model Test"""

#     def setUp(self):
#         self.rancher_user = baker.make(
#             "account.User", phone="09151498722", fullName="Hamid Balalzadeh"
#         )
#         self.rancher = Rancher.objects.get(user=self.rancher_user)

#         self.veterinarian_user = baker.make("account.User", phone="09151498721")
#         self.veterinary = baker.make(Veterinarian, user=self.veterinarian_user)

#         self.request = baker.make(
#             Request, rancher=self.rancher, veterinarian=self.veterinary
#         )

#         self.payload = {"image": "test.png"}

#         self.model = RequestImage.objects.create(request=self.request, **self.payload)

#     def test_create_model_should_work_properly(self):
#         """Test create model"""
#         for k, v in self.payload.items():
#             self.assertEqual(getattr(self.model, k), v)

#         self.assertEqual(self.model.request, self.request)
