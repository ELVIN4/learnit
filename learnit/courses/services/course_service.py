from django.http import Http404
from django.core.cache import cache
from django.db.models import Q
from django.shortcuts import get_object_or_404
from courses.models import Course, Language


def get_courses_in_category(
    category, subcategories, paginate_by, page_number, language, cache_timeout=60 * 25
):
    cache_key = (
        f"category_{category.slug}_page_{paginate_by}_lang_{language}_{page_number}"
    )
    queryset = cache.get(cache_key)

    if not queryset:
        queryset = (
            Course.objects.filter(Q(category=category) | Q(category__in=subcategories))
            .filter(is_published=True)
            .order_by("-priority", "-average_views", "-modified_date")
        )
        cache.set(cache_key, queryset, timeout=cache_timeout)

    return queryset


def get_courses_by_author(author_id, page_number, cache_timeout=60 * 25):
    cache_key = f"author_courses_{author_id}_page_{page_number}"
    courses = cache.get(cache_key)

    if not courses:
        courses = Course.objects.filter(
            Q(author_id=author_id) & Q(is_published=True)
        ).order_by("-priority")
        if courses.exists():
            cache.set(cache_key, courses, timeout=cache_timeout)
        else:
            raise Http404()

    return courses


def get_courses_by_language(language_code):
    current_language = get_object_or_404(Language, code=language_code)
    return Course.objects.filter(language=current_language, is_published=True)


def get_popular_courses(courses, limit=5):
    return courses.order_by("-average_views")[:limit]


def get_new_courses(courses, limit=5):
    return courses.order_by("-modified_date")[:limit]
