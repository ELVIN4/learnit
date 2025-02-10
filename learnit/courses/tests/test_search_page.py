from django.test import TestCase
from django.urls import reverse
from django.utils.translation import activate
from ..models import Course, Category, Language


class SearchPageTest(TestCase):
    def setUp(self):
        self.language = Language.objects.create(name="English", code="en")
        activate("en")
        self.category = Category.objects.create(
            name="Programming", language=self.language, is_published=True
        )
        self.course = Course.objects.create(
            name="Django for Beginners",
            category=self.category,
            thumbnail="https://y.image.com/testLearnIT",
            lessons_count=0,
            language=self.language,
            is_published=True,
        )

    def test_search_page_status_code(self):
        response = self.client.get(reverse("search"))
        self.assertEqual(response.status_code, 200)

    def test_search_with_query(self):
        response = self.client.get(reverse("search") + "?q=django")
        self.assertIn("courses", response.context)
        self.assertIn("categories", response.context)
        self.assertEqual(len(response.context["courses"]), 1)
        self.assertEqual(response.context["courses"][0], self.course)

    def test_search_with_no_results(self):
        response = self.client.get(reverse("search") + "?q=nonexistent")
        self.assertEqual(len(response.context["courses"]), 0)
        self.assertEqual(len(response.context["categories"]), 0)
        self.assertEqual(response.context["result_count"], 0)

    def test_search_with_empty_query(self):
        response = self.client.get(reverse("search") + "?q=")
        self.assertEqual(len(response.context["courses"]), 1)
        self.assertEqual(len(response.context["categories"]), 1)
        self.assertEqual(response.context["result_count"], 2)

    def test_context_includes_query(self):
        response = self.client.get(reverse("search") + "?q=django")
        self.assertEqual(response.context["q"], "django")

    def test_result_count(self):
        response = self.client.get(reverse("search") + "?q=django")
        self.assertEqual(response.context["result_count"], 1)
