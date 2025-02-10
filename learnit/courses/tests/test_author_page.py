from django.test import TestCase
from django.urls import reverse
from django.core.cache import cache
from courses.models import Course, Category, Language


class AuthorPageTest(TestCase):
    def setUp(self):
        cache.clear()

        self.language = Language.objects.create(name="English", code="en")
        self.category = Category.objects.create(
            name="Programming", language=self.language
        )
        self.course = Course.objects.create(
            name="Django for Beginners",
            author="John Doe",
            author_id="123",
            url="https://example.com",
            thumbnail="https://y.image.com/testLearnIT",
            lessons_count=10,
            category=self.category,
            language=self.language,
        )

    def test_author_page_status_code(self):
        response = self.client.get(reverse("author", kwargs={"author_id": "123"}))
        self.assertEqual(response.status_code, 200)

    def test_courses_in_context(self):
        response = self.client.get(reverse("author", kwargs={"author_id": "123"}))
        self.assertIn("courses", response.context)
        self.assertEqual(len(response.context["courses"]), 1)

    def test_404_on_nonexistent_author(self):
        response = self.client.get(reverse("author", kwargs={"author_id": "999"}))
        self.assertEqual(response.status_code, 404)
