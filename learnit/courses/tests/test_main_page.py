from django.test import TestCase
from django.urls import reverse
from django.core.cache import cache
from courses.models import Course, Category, Language


class MainPageTest(TestCase):
    def setUp(self):
        cache.clear()

        self.language = Language.objects.create(name="English", code="en")
        self.category = Category.objects.create(
            name="Programming", language=self.language
        )
        self.course = Course.objects.create(
            name="Django for Beginners",
            url="https://example.com",
            lessons_count=10,
            author="John Doe",
            category=self.category,
            language=self.language,
        )

    def test_main_page_status_code(self):
        response = self.client.get(reverse("main"))
        self.assertEqual(response.status_code, 200)

    def test_courses_in_context(self):
        response = self.client.get(reverse("main"))
        self.assertIn("courses", response.context)
        self.assertEqual(len(response.context["courses"]), 1)

    def test_categories_in_context(self):
        response = self.client.get(reverse("main"))
        self.assertIn("categories", response.context)
        self.assertEqual(len(response.context["categories"]), 1)
