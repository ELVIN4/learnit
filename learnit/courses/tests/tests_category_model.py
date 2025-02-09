# Create your tests here.
from django.test import TestCase
from courses.models import Category, Language


class CategoryModelTest(TestCase):
    def setUp(self):
        self.language = Language.objects.create(name="English", code="en")

        self.parent_category = Category.objects.create(
            name="Parent Category",
            slug="parent-category",
            priority=1,
            language=self.language,
            is_published=True,
        )

        self.child_category = Category.objects.create(
            name="Child Category",
            slug="child-category",
            priority=2,
            parent_category=self.parent_category,
            language=self.language,
            is_published=True,
        )

    def test_category_creation(self):
        """
        Проверяем, что категории создаются корректно и связь через ForeignKey работает.
        """
        self.assertEqual(self.parent_category.name, "Parent Category")
        self.assertEqual(self.child_category.name, "Child Category")
        self.assertEqual(self.child_category.parent_category, self.parent_category)
        self.assertEqual(self.child_category.language, self.language)
        self.assertTrue(self.parent_category.is_published)
        self.assertTrue(self.child_category.is_published)

    def test_category_str_method(self):
        """
        Проверяем корректность метода __str__, который должен возвращать имя категории.
        """
        self.assertEqual(str(self.parent_category), "Parent Category")
        self.assertEqual(str(self.child_category), "Child Category")

    def test_default_priority(self):
        """
        Проверяем, что поле priority по умолчанию равно 0, если не указано.
        """
        default_priority_category = Category.objects.create(
            name="No Priority Category",
            slug="no-priority-category",
            language=self.language,
            is_published=False,
        )
        self.assertEqual(default_priority_category.priority, 0)

    def test_category_parent_null(self):
        """
        Проверяем, что категория может не иметь родительской категории (parent_category).
        """
        category_without_parent = Category.objects.create(
            name="No Parent Category",
            slug="no-parent-category",
            priority=3,
            language=self.language,
            is_published=True,
        )
        self.assertIsNone(category_without_parent.parent_category)

    def test_protect_on_delete_parent_category(self):
        """
        Проверяем, что при попытке удалить родительскую категорию происходит ошибка из-за on_delete=PROTECT.
        """
        with self.assertRaises(Exception):
            self.parent_category.delete()
