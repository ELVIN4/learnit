from django.test import TestCase
from courses.models import Category, Language


class CategoryModelTest(TestCase):
    def setUp(self):
        self.language = Language.objects.create(name="English", code="en")
        self.category = Category.objects.create(
            name="Programming", language=self.language
        )

    def test_category_creation(self):
        self.assertIsInstance(self.category, Category)
        self.assertEqual(self.category.name, "Programming")

    def test_category_slug_generated(self):
        self.assertEqual(self.category.slug, "programming-en")

    def test_category_str(self):
        self.assertEqual(str(self.category), "Programming")

    def test_parent_category(self):
        parent = Category.objects.create(name="Technology", language=self.language)
        self.category.parent_category = parent
        self.category.save()
        self.assertEqual(self.category.parent_category.name, "Technology")
