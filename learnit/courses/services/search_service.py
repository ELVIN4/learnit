from django.db.models import Q
from courses.models import Category, Course
from django.utils.translation import get_language


def search_categories_and_courses(query):
    """
    Performs search for categories and courses based on the provided query
    and the current language. Returns categories and courses ordered by priority.
    """
    current_language_code = get_language()

    categories = Category.objects.filter(
        Q(name__icontains=query)
        & Q(language__code=current_language_code)
        & Q(is_published=True)
    ).order_by("-priority")

    courses = Course.objects.filter(
        Q(name__icontains=query)
        & Q(language__code=current_language_code)
        & Q(is_published=True)
    ).order_by("-priority", "-average_views")

    return categories, courses
