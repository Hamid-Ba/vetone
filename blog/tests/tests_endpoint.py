from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from blog import models


class BlogTestCase(APITestCase):
    def setUp(self):
        self.blog1 = models.Blog.objects.create(
            title="Blog 1",
            slug="blog-1",
        )
        self.blog2 = models.Blog.objects.create(
            title="Blog 2",
            slug="blog-2",
        )

    def test_blog_detail_view(self):
        url = reverse("blog:blog_detail", args=[self.blog1.slug])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["slug"], self.blog1.slug)

    def test_blogs_view(self):
        url = reverse("blog:blogs-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][0]["title"], self.blog2.title)

    def test_latest_blogs_view(self):
        url = reverse("blog:latest-blogs-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["title"], self.blog2.title)
