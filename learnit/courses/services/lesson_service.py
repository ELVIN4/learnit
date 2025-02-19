from django.core.cache import cache
from django.db.models import Q
from django.shortcuts import get_object_or_404
from courses.models import Lesson


def get_lessons_for_course(course):
    cache_key = f"lessons_for_course_{course.slug}"
    lessons = cache.get(cache_key)

    if not lessons:
        lessons = Lesson.objects.filter(Q(course=course) & Q(is_published=True))
        cache.set(cache_key, lessons, timeout=60 * 25)

    return lessons


def get_lesson(course_slug, lesson_order, cache_timeout=60 * 25):
    lesson_cache_key = f"lesson_{lesson_order}_for_{course_slug}"
    lesson = cache.get(lesson_cache_key)
    if not lesson:
        lesson = get_object_or_404(Lesson, course__slug=course_slug, order=lesson_order)
        cache.set(lesson_cache_key, lesson, timeout=cache_timeout)

    return lesson
