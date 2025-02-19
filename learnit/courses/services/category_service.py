from django.core.cache import cache
from django.db.models import Q
from django.shortcuts import get_object_or_404
from courses.models import Category, Language


def get_top_categories_by_language(language_code, limit=20):
    current_language = get_object_or_404(Language, code=language_code)
    return Category.objects.filter(
        parent_category=None,
        language=current_language,
        is_published=True,
    ).order_by("-priority")[:limit]


def get_category_with_subcategories(category_slug, cache_timeout=60 * 60):
    category = get_object_or_404(Category, slug=category_slug)
    subcategories_cache_key = f"category_{category.slug}_all_subcategories"
    subcategories = cache.get(subcategories_cache_key)

    if not subcategories:
        subcategories = get_all_subcategories(category)
        cache.set(subcategories_cache_key, subcategories, timeout=cache_timeout)
    return category, subcategories


def get_category_with_parent_category(parent_category, cache_timeout=60 * 25):
    child_cache_key = f"child_categories_{parent_category}"
    categories = cache.get(child_cache_key)

    if not categories:
        categories = Category.objects.filter(parent_category=parent_category)
        cache.set(child_cache_key, categories, timeout=cache_timeout)

    return categories


def get_all_subcategories(category):
    subcategories = [category]
    children = Category.objects.filter(parent_category=category, is_published=True)
    for child in children:
        subcategories.extend(get_all_subcategories(child))  # recursive
    return subcategories


def get_all_categories(language_code, cache_timeout=60 * 25):
    cache_key = f"all_categories_{language_code}"
    categories = cache.get(cache_key)

    if not categories:
        current_language = get_object_or_404(Language, code=language_code)
        categories = Category.objects.filter(
            Q(is_published=True) & Q(language=current_language)
        ).order_by("-priority", "-parent_category")
        cache.set(cache_key, categories, timeout=cache_timeout)

    return categories
