from django.views.generic import TemplateView, ListView, DetailView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.utils.translation import get_language
from django.urls import reverse

from .mixins.breadcrumbs_mixin import BreadcrumbsMixin
from .models import Course
from .services.lesson_service import get_lessons_for_course, get_lesson
from .services.search_service import search_categories_and_courses
from .services.category_service import (
    get_top_categories_by_language,
    get_category_with_subcategories,
    get_category_with_parent_category,
    get_all_categories,
)
from .services.course_service import (
    get_courses_by_author,
    get_courses_in_category,
    get_new_courses,
    get_popular_courses,
    get_courses_by_language,
)


class MainPage(TemplateView):
    """
    This class handles the display of the main page of the courses section.

    It retrieves and displays all published courses in the current language,
    along with the top 15 categories that have no parent category.

    The main page also showcases the 5 most popular courses (based on average views) and the 5 most recently updated courses.

    The page is cached for 25 minutes.
    """

    template_name = "courses/base.html"

    @method_decorator(
        cache_page(
            60 * 25,
            key_prefix=lambda self, *args, **kwargs: f"main_page_{get_language()}",
        )
    )
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        current_language_code = get_language()
        courses = get_courses_by_language(current_language_code)
        categories = get_top_categories_by_language(current_language_code)

        popular_courses = get_popular_courses(courses)
        new_courses = get_new_courses(courses)

        context = super().get_context_data(**kwargs)
        context.update(
            {
                "courses": courses,
                "categories": categories,
                "popular_courses": popular_courses,
                "new_courses": new_courses,
            }
        )

        return context


class CategoryPage(BreadcrumbsMixin, ListView):
    """
    This class handles the display of all courses within a specific category.

    It retrieves courses that belong to the specified category or any of its child categories.

    The view also includes breadcrumbs to help navigate through the category hierarchy.

    The categories are cached for 25 minutes.
    """

    template_name = "courses/category.html"
    context_object_name = "courses"
    paginate_by = 50

    def get_queryset(self):
        category_slug = self.kwargs["category"]
        category, subcategories = get_category_with_subcategories(category_slug)
        self.category = category
        self.child_categories = get_category_with_parent_category(
            parent_category=category
        )

        return get_courses_in_category(
            category,
            subcategories,
            self.paginate_by,
            self.request.GET.get("page", 1),
            get_language(),
            cache_timeout=60 * 25,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "category": self.category,
                "child_categories": self.child_categories,
                "breadcrumbs": self.get_breadcrumbs(),
            }
        )

        return context

    def get_breadcrumbs(self):
        breadcrumbs = super().get_breadcrumbs()
        categories = [self.category]
        parent_category = self.category.parent_category

        while parent_category:
            categories.insert(0, parent_category)
            parent_category = parent_category.parent_category

        for category in categories:
            breadcrumbs.append(
                {
                    "name": category.name,
                    "url": reverse("category", kwargs={"category": category.slug}),
                }
            )
        return breadcrumbs


class CoursePage(DetailView):
    """
    This class handles the display of all lessons within a specific course.

    It retrieves the course details based on the provided slug and displays all published lessons associated with that course.

    The lessons are cached for 25 minutes.

    """

    model = Course
    template_name = "courses/course.html"
    context_object_name = "course"
    slug_field = "slug"
    slug_url_kwarg = "course_slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.object
        context["lessons"] = get_lessons_for_course(course)

        return context


class LessonPage(TemplateView):
    template_name = "courses/lesson.html"
    context_object_name = "lesson"
    slug_url_kwarg = "course_slug"
    slug_field = "course__slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_slug = self.kwargs["course_slug"]
        lesson_order = self.kwargs["lesson_order"]
        lesson = get_lesson(course_slug, lesson_order, cache_timeout=60 * 25)
        context["lesson"] = lesson

        return context


class AuthorPage(ListView):
    """
    This class handles the display of all courses by a specific author.

    It retrieves and displays all courses associated with the given author.  If no courses are found for the author, a 404 error is raised.

    The page also includes an additional context variable to indicate that this is the author's page.

    The courses are cached for 25 minutes.
    """

    template_name = "courses/author.html"
    context_object_name = "courses"
    paginate_by = 50

    def get_queryset(self):
        author_id = self.kwargs["author_id"]
        return get_courses_by_author(
            author_id, self.request.GET.get("page", 1), cache_timeout=60 * 25
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["author_page"] = True
        return context


class AllCategoriesPage(ListView):
    """
    This class display all categories on the page.

    Categories filtered by language and publication status.

    The courses are cached for 25 minutes.
    """

    template_name = "courses/all_categories.html"
    context_object_name = "categories"

    def get_queryset(self):
        return get_all_categories(get_language())


class SearchPage(ListView):
    template_name = "courses/search.html"

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        query = self.request.GET.get("q", "")

        categories, courses = search_categories_and_courses(query)

        context["categories"] = categories
        context["courses"] = courses
        context["result_count"] = categories.count() + courses.count()
        context["q"] = query

        return context
