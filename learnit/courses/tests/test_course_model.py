from django.test import TestCase
from courses.models import Course, Category, Language


class CourseModelTest(TestCase):
    def setUp(self):
        self.language = Language.objects.create(name="English", code="en")
        self.category = Category.objects.create(
            name="Programming", language=self.language
        )
        self.course = Course.objects.create(
            name="Django for Beginners",
            url="https://example.com",
            thumbnail="https://y.image.com/testLearnIT",
            lessons_count=10,
            author="John Doe",
            category=self.category,
            language=self.language,
        )

    def test_course_creation(self):
        self.assertIsInstance(self.course, Course)
        self.assertEqual(self.course.name, "Django for Beginners")

    def test_course_slug_generated(self):
        self.assertEqual(self.course.slug, "django-for-beginners-en")

    def test_course_str(self):
        self.assertEqual(str(self.course), "Django for Beginners")

    def test_course_related_category(self):
        self.assertEqual(self.course.category.name, "Programming")
