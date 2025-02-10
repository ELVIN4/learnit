from django.test import TestCase
from django.urls import reverse
from django.core.cache import cache
from courses.models import Lesson, Course, Category, Language


class LessonPageTest(TestCase):
    def setUp(self):
        cache.clear()

        self.language = Language.objects.create(name="English", code="en")
        self.category = Category.objects.create(
            name="Programming", language=self.language
        )
        self.course = Course.objects.create(
            name="Django for Beginners",
            slug="django-for-beginners",
            url="https://example.com",
            thumbnail="https://y.image.com/testLearnIT",
            lessons_count=10,
            author="John Doe",
            category=self.category,
            language=self.language,
        )
        self.lesson = Lesson.objects.create(
            name="Introduction",
            course=self.course,
            thumbnail="https://y.image.com/testLearnIT",
            video_id="12345",
            order=1,
        )

    def test_lesson_page_status_code(self):
        response = self.client.get(
            reverse(
                "lesson", kwargs={"course_slug": self.course.slug, "lesson_order": 1}
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_lesson_in_context(self):
        response = self.client.get(
            reverse(
                "lesson", kwargs={"course_slug": self.course.slug, "lesson_order": 1}
            )
        )
        self.assertIn("lesson", response.context)
        self.assertEqual(response.context["lesson"].name, "Introduction")
