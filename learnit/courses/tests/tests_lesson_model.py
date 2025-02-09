from django.test import TestCase
from django.utils import timezone
from courses.models import Lesson, Course, Category, Language


class LessonModelTest(TestCase):
    def setUp(self):
        self.language = Language.objects.create(
            name="Russian",
            code="ru",
            priority=0,
            is_published=True,
        )
        self.category = Category.objects.create(
            name="Child Category",
            slug="child-category",
            priority=2,
            language=self.language,
            is_published=True,
        )

        self.course = Course.objects.create(
            name="Random Course",
            slug="random-course",
            thumbnail="http://example.com/thumbnail.jpg",
            description="This is a random course created with sample data.",
            url="http://youtube.com/random-course",
            lessons_count=10,
            author="John Doe",
            author_id="123e4567-e89b-12d3-a456-426614174000",
            category=self.category,
            total_views=5000,
            average_views=500,
            total_duration=1200,
            language=self.language,
            is_published=True,
            priority=5,
            upload_date=timezone.now().date(),
            update_date=timezone.now().date(),
            modified_date=timezone.now().date(),
        )

    def test_lesson_creation_with_required_fields(self):
        # Тестируем создание урока с обязательными полями
        lesson = Lesson.objects.create(
            name="Test Lesson",
            course=self.course,
            video_id="some_video_id",
            thumbnail="http://example.com/thumbnail.jpg",
        )
        self.assertEqual(lesson.name, "Test Lesson")
        self.assertEqual(lesson.course, self.course)
        self.assertEqual(lesson.video_id, "some_video_id")
        self.assertEqual(lesson.thumbnail, "http://example.com/thumbnail.jpg")
        self.assertEqual(lesson.views, 0)  # Default value
        self.assertEqual(lesson.likes, 0)  # Default value
        self.assertEqual(lesson.duration, 0)  # Default value

    def test_order_is_set_automatically(self):
        # Тестируем, что поле "order" автоматически увеличивается
        lesson1 = Lesson.objects.create(
            name="First Lesson",
            course=self.course,
            video_id="video1",
            thumbnail="http://example.com/thumbnail1.jpg",
        )
        lesson2 = Lesson.objects.create(
            name="Second Lesson",
            course=self.course,
            video_id="video2",
            thumbnail="http://example.com/thumbnail2.jpg",
        )

        self.assertEqual(lesson1.order, 1)
        self.assertEqual(lesson2.order, 2)

    def test_save_sets_order_if_not_provided(self):
        # Тестируем, что если "order" не задан, он ставится автоматически
        lesson1 = Lesson.objects.create(
            name="First Lesson",
            course=self.course,
            video_id="video1",
            thumbnail="http://example.com/thumbnail1.jpg",
        )
        lesson2 = Lesson.objects.create(
            name="Second Lesson",
            course=self.course,
            video_id="video2",
            thumbnail="http://example.com/thumbnail2.jpg",
        )

        # Проверяем, что order увеличивается автоматически
        self.assertEqual(lesson1.order, 1)
        self.assertEqual(lesson2.order, 2)

    def test_save_without_order_sets_first_order(self):
        # Тестируем, что если урок первый в курсе, его порядок ставится 1
        lesson = Lesson.objects.create(
            name="First Lesson",
            course=self.course,
            video_id="video1",
            thumbnail="http://example.com/thumbnail1.jpg",
        )
        self.assertEqual(lesson.order, 1)

    def test_lesson_str_method(self):
        # Тестируем метод __str__
        lesson = Lesson.objects.create(
            name="Test Lesson",
            course=self.course,
            video_id="video_id",
            thumbnail="http://example.com/thumbnail.jpg",
        )
        self.assertEqual(str(lesson), "Test Lesson")
