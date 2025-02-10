from django.shortcuts import get_object_or_404
from django.http import Http404
from django.views.generic import TemplateView, ListView, DetailView
from django.urls import reverse
from django.utils.translation import get_language
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from .models import Course, Category, Lesson, Language
from .mixins.breadcrumbs_mixin import BreadcrumbsMixin


class MainPage(TemplateView):
    """
    This class handles the display of the main page of the courses section.

    It retrieves and displays all published courses in the current language,
    along with the top 15 categories that have no parent category.

    The main page also showcases the 5 most popular courses (based on average views) and the 5 most recently updated courses.

    The page is cached for 25 minutes.
    """

    template_name = "courses/base.html"

    # Cache for 25 minutes with a unique key for each language
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
        current_language = get_object_or_404(Language, code=current_language_code)

        courses = Course.objects.filter(language=current_language, is_published=True)
        categories = Category.objects.filter(
            parent_category=None,
            language=current_language,
            is_published=True,
        ).order_by("-priority")[:15]  # top 15 categories that have no parent category

        popular_courses = courses.order_by("-average_views")[:5]
        new_courses = courses.order_by("-modified_date")[:5]

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

    model = Course
    template_name = "courses/category.html"
    context_object_name = "courses"
    paginate_by = 50

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs["category"])
        child_categories = Category.objects.filter(parent_category=category)

        cache_key = f"category_{category.slug}_page_{self.paginate_by}_lang_{get_language()}_{self.request.GET.get('page', 1)}"
        queryset = cache.get(cache_key)

        if not queryset:
            queryset = (
                Course.objects.filter(
                    Q(category=category) | Q(category__in=child_categories)
                )
                .filter(is_published=True)
                .order_by(
                    "-priority",
                    "-average_views",
                    "-modified_date",
                )
            )
            cache.set(cache_key, queryset, timeout=60 * 25)

        self.category = category
        self.child_categories = child_categories

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["category"] = self.category
        context["child_categories"] = self.child_categories

        context["breadcrumbs"] = self.get_breadcrumbs()

        return context

    def get_breadcrumbs(self):
        breadcrumbs = super().get_breadcrumbs()

        categories = [self.category]

        parent_category = self.category.parent_category
        while parent_category:
            categories.insert(
                0, parent_category
            )  # Inserted at the beginning to make them closer to the current category
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

        cache_key = f"lessons_for_course_{course.slug}"
        lessons = cache.get(cache_key)

        if not lessons:
            lessons = Lesson.objects.filter(Q(course=course) & Q(is_published=True))
            cache.set(cache_key, lessons, timeout=60 * 25)

        context["lessons"] = lessons
        return context


class LessonPage(DetailView):
    """
    This class handles the display of a specific lesson within a course, identified by its order.

    It retrieves the lesson based on the provided course slug and lesson order.

    The lesson is cached for 25 minutes. If the lesson is not found, a 404 error is raised.
    """

    model = Lesson
    template_name = "courses/lesson.html"
    context_object_name = "lesson"
    slug_url_kwarg = "course_slug"
    slug_field = "course__slug"

    def get_queryset(self):
        course_slug = self.kwargs["course_slug"]
        lesson_order = self.kwargs["lesson_order"]

        cache_key = f"lesson_{course_slug}_{lesson_order}"
        lesson = cache.get(cache_key)

        if not lesson:
            lesson = Lesson.objects.filter(
                course__slug=course_slug, order=lesson_order
            ).first()
            if not lesson:
                raise Http404()

            cache.set(cache_key, lesson, timeout=60 * 25)

        return Lesson.objects.filter(course__slug=course_slug, order=lesson_order)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AuthorPage(ListView):
    """
    This class handles the display of all courses by a specific author.

    It retrieves and displays all courses associated with the given author.  If no courses are found for the author, a 404 error is raised.

    The page also includes an additional context variable to indicate that this is the author's page.

    The courses are cached for 25 minutes.
    """

    model = Course
    template_name = "courses/author.html"
    context_object_name = "courses"
    paginate_by = 50

    def get_queryset(self):
        author_id = self.kwargs["author_id"]

        cache_key = f"author_courses_{author_id}_page_{self.request.GET.get('page', 1)}"
        courses = cache.get(cache_key)

        if not courses:
            courses = Course.objects.filter(
                Q(author_id=author_id) & Q(is_published=True)
            ).order_by("-priority")
            if not courses.exists():
                raise Http404()

            cache.set(cache_key, courses, timeout=60 * 25)

        return courses

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["author_page"] = True
        return context


# TO DO use elasticsearch
class SearchPage(ListView):
    template_name = "courses/search.html"

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_language_code = get_language()

        query = self.request.GET.get("q", "")

        context["categories"] = Category.objects.filter(
            Q(name__icontains=query)
            & Q(language__code=current_language_code)
            & Q(is_published=True)
        ).order_by("-priority")

        context["courses"] = Course.objects.filter(
            Q(name__icontains=query)
            & Q(language__code=current_language_code)
            & Q(is_published=True)
        ).order_by("-priority", "-average_views")

        context["result_count"] = (
            context["categories"].count() + context["courses"].count()
        )
        context["q"] = query

        return context
