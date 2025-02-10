from django.test import TestCase
from django.urls import reverse
from django.core.cache import cache
from courses.models import Category, Course, Language


class CategoryPageTest(TestCase):
    def setUp(self):
        cache.clear()
        self.language = Language.objects.create(name="English", code="en")
        self.category = Category.objects.create(
            name="Programming", slug="programming", language=self.language
        )
        self.course = Course.objects.create(
            name="Django for Beginners",
            url="https://example.com",
            lessons_count=10,
            thumbnail="https://y.image.com/testLearnIT",
            author="John Doe",
            category=self.category,
            language=self.language,
        )

    def test_category_page_status_code(self):
        response = self.client.get(
            reverse("category", kwargs={"category": self.category.slug})
        )
        self.assertEqual(response.status_code, 200)

    def test_courses_in_context(self):
        response = self.client.get(
            reverse("category", kwargs={"category": self.category.slug})
        )
        self.assertIn("courses", response.context)
        self.assertEqual(len(response.context["courses"]), 1)

    def test_breadcrumbs_in_context(self):
        response = self.client.get(
            reverse("category", kwargs={"category": self.category.slug})
        )
        self.assertIn("breadcrumbs", response.context)
        self.assertEqual(
            response.context["breadcrumbs"][-1]["name"], self.category.name
        )

    def test_404_on_nonexistent_category(self):
        response = self.client.get(
            reverse("category", kwargs={"category": "nonexistent-category"})
        )
        self.assertEqual(response.status_code, 404)
