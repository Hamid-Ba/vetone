"""
Test Blog Module Models
"""
from django.test import TestCase

from blog import models


class BlogModelTest(TestCase):
    """Blog Model Test"""

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        models.Blog.objects.create(
            title="TestBlog",
            slug="test-blog",
            short_desc="Short description",
            desc="Long description",
            image_alt="Test Alt",
            image_title="Test Title",
        )

    def test_title_label(self):
        blog = models.Blog.objects.filter(title="TestBlog").first()
        field_label = blog._meta.get_field("title").verbose_name
        self.assertEqual(field_label, "عنوان")

    def test_slug_max_length(self):
        blog = models.Blog.objects.filter(title="TestBlog").first()
        max_length = blog._meta.get_field("slug").max_length
        self.assertEqual(max_length, 170)

    def test_object_name_is_title(self):
        blog = models.Blog.objects.filter(title="TestBlog").first()
        expected_object_name = f"{blog.title}"
        self.assertEqual(expected_object_name, str(blog))

    def test_short_desc_blank(self):
        blog = models.Blog.objects.filter(title="TestBlog").first()
        short_desc = blog._meta.get_field("short_desc").blank
        self.assertTrue(short_desc)

    def test_desc_null(self):
        blog = models.Blog.objects.filter(title="TestBlog").first()
        desc = blog._meta.get_field("desc").null
        self.assertTrue(desc)

    def test_image_alt_max_length(self):
        blog = models.Blog.objects.filter(title="TestBlog").first()
        max_length = blog._meta.get_field("image_alt").max_length
        self.assertEqual(max_length, 72)

    def test_image_related_name(self):
        blog = models.Blog.objects.filter(title="TestBlog").first()
        related_name = blog._meta.get_field("image").related_query_name()
        self.assertEqual(related_name, "blogs")


# class SpecificationModelTest(TestCase):
#     """Blog Model Test"""

#     @classmethod
#     def setUpTestData(cls):
#         category = create_category("Test")
#         models.Blog.objects.create(
#             title="TestBlog", slug="test-blog", category=category
#         )

#         # Set up non-modified objects used by all test methods
#         models.Specification.objects.create(
#             key="TestKey",
#             value="TestValue",
#             blog=models.Blog.objects.filter(title="TestBlog").first(),
#         )

#     def test_type_default_value(self):
#         spec = models.Specification.objects.get(id=1)
#         default_type = spec.type
#         self.assertEquals(default_type, "TS")

#     def test_key_max_length(self):
#         spec = models.Specification.objects.get(id=1)
#         max_length = spec._meta.get_field("key").max_length
#         self.assertEquals(max_length, 125)

#     def test_value_blank_false(self):
#         spec = models.Specification.objects.get(id=1)
#         blank = spec._meta.get_field("value").blank
#         self.assertFalse(blank)

#     def test_object_name(self):
#         spec = models.Specification.objects.get(id=1)
#         expected_object_name = f"{spec.blog.title}-{spec.key}"
#         self.assertEquals(expected_object_name, str(spec))
