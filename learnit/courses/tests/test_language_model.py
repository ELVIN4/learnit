from django.test import TestCase
from courses.models import Language


class LanguageModelTest(TestCase):
    def setUp(self):
        self.language = Language.objects.create(name="English", code="en")

    def test_language_creation(self):
        self.assertIsInstance(self.language, Language)
        self.assertEqual(self.language.name, "English")
        self.assertEqual(self.language.code, "en")

    def test_language_str(self):
        self.assertEqual(str(self.language), "English")
