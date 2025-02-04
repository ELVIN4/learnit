from django import template

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