from django.test import TestCase
from courses.models import Lesson, Course, Category, Language


class LessonModelTest(TestCase):
    def setUp(self):
        self.language = Language.objects.create(name="English", code="en")
        self.category = Category.objects.create(
            name="Programming", language=self.language
        )
        self.course = Course.objects.create(
            name="Django for Beginners",
            url="https://example.com",
            lessons_count=10,
            author="John Doe",
            thumbnail="https://y.image.com/testLearnIT",
            category=self.category,
            language=self.language,
        )
        self.lesson = Lesson.objects.create(
            name="Introduction",
            video_id="12345",
            course=self.course,
            thumbnail="https://y.image.com/testLearnIT",
            order=1,
        )

    def test_lesson_creation(self):
        self.assertIsInstance(self.lesson, Lesson)
        self.assertEqual(self.lesson.name, "Introduction")

    def test_lesson_order(self):
        self.assertEqual(self.lesson.order, 1)

    def test_lesson_str(self):
        self.assertEqual(str(self.lesson), "Introduction")

    def test_related_course(self):
        self.assertEqual(self.lesson.course.name, "Django for Beginners")
