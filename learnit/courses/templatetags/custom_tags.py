from django import template
from courses.models import Course

register = template.Library()


@register.filter
def percentage(value, total):
    try:
        return round((value / total) * 100)
    except (ZeroDivisionError, TypeError):
        return 0


@register.filter
def seconds_to_hours(seconds):
    try:
        hours = seconds // 3600
        return hours
    except Exception as e:
        print(e)
        return None


@register.filter
def seconds_to_minutes(seconds):
    try:
        hours = seconds // 60
        return hours
    except Exception as e:
        print(e)
        return None


@register.simple_tag
def count_courses_by_language(language_code):
    return Course.objects.filter(language__code=language_code).count()
