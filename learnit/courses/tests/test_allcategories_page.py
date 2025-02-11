from django.test import TestCase
from django.urls import reverse
from django.core.cache import cache
from django.utils.translation import activate
from courses.models import Category, Language


class AllCategoriesPageTest(TestCase):
    def setUp(self):
        cache.clear()

        self.language = Language.objects.create(name="English", code="en")
        self.language_other = Language.objects.create(name="German", code="de")
        self.category_1 = Category.objects.create(
            name="Programming",
            language=self.language,
            is_published=True,
            priority=1,
        )
        self.category_2 = Category.objects.create(
            name="Web Development",
            language=self.language,
            is_published=True,
            priority=2,
        )
        self.category_3 = Category.objects.create(
            name="Cooking",
            language=self.language_other,
            is_published=True,
            priority=3,
        )
        activate("en")  # Устанавливаем текущий язык для тестов

    def test_page_status_code(self):
        response = self.client.get(reverse("categories"))
        self.assertEqual(response.status_code, 200)

    def test_categories_filtered_by_language_and_published(self):
        response = self.client.get(reverse("categories"))
        categories = response.context["categories"]

        # Проверяем, что только категории для текущего языка и опубликованные
        self.assertIn(self.category_1, categories)
        self.assertIn(self.category_2, categories)
        self.assertNotIn(self.category_3, categories)
