from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views import View
from django.views.generic import TemplateView, ListView
from django.urls import reverse
from django.utils.translation import get_language
from django.db.models import Q
from .models import Course, Category, Lesson, Language
from .mixins.breadcrumbs_mixin import BreadcrumbsMixin


class MainPage(TemplateView):
    """Главная страница курсов"""

    template_name = "courses/base.html"

    def get_context_data(self, **kwargs):
        current_language_code = get_language()
        current_language = get_object_or_404(Language, code=current_language_code)

        # Получаем курсы и категории для текущего языка
        courses = Course.objects.filter(language=current_language, is_published=True)
        categories = Category.objects.filter(
            parent_category=None,
            language=current_language,
            is_published=True,
        ).order_by("-priority")[:15]

        popular_courses = courses.order_by("-average_views")[:5]
        new_courses = courses.order_by("-modified_date")[:5]

        context = super().get_context_data(**kwargs)

        # Добавляем курсы и категории в контекст
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
    """Вывод всех курсов по категории"""

    model = Course
    template_name = "courses/category.html"
    context_object_name = "courses"
    paginate_by = 20

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs["category"])
        child_categories = Category.objects.filter(parent_category=category)

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

        self.category = category
        self.child_categories = child_categories

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Добавляем в контекст текущую категорию и дочерние категории
        context["category"] = self.category
        context["child_categories"] = self.child_categories

        # Получаем хлебные крошки с учетом текущей категории
        context["breadcrumbs"] = self.get_breadcrumbs()

        return context

    def get_breadcrumbs(self):
        # Получаем хлебные крошки из миксина
        breadcrumbs = super().get_breadcrumbs()

        categories = [self.category]
        # Добавляем родительские категории (если есть)
        parent_category = self.category.parent_category
        while parent_category:
            categories.insert(
                0, parent_category
            )  # Вставляем в начало, чтобы они шли до текущей категории
            parent_category = parent_category.parent_category

        # Добавляем текущую категорию в хлебные крошки
        for category in categories:
            breadcrumbs.append(
                {
                    "name": category.name,
                    "url": reverse("category", kwargs={"category": category.slug}),
                }
            )
        return breadcrumbs


class CoursePage(View):
    """Вывод всех уроков по курсу"""

    def get(self, request, course_slug):
        course = get_object_or_404(Course, slug=course_slug)
        lessons = Lesson.objects.filter(course=course)

        return render(
            request,
            "courses/course.html",
            context={"lessons": lessons, "course": course},
        )


class LessonPage(View):
    def get(self, request, course_slug, lesson_order):
        lesson = get_object_or_404(
            Lesson.objects.filter(course__slug=course_slug, order=lesson_order)
        )

        return render(request, "courses/lesson.html", context={"lesson": lesson})


class AuthorPage(View):
    def get(self, request, author_id):
        courses = Course.objects.filter(author_id=author_id)

        if not courses.exists():
            raise Http404()

        return render(
            request,
            "courses/author.html",
            context={
                "courses": courses,
                "author_page": True,
            },
        )


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
        )
        context["courses"] = Course.objects.filter(
            Q(name__icontains=query)
            & Q(language__code=current_language_code)
            & Q(is_published=True)
        )

        context["result_count"] = (
            context["categories"].count() + context["courses"].count()
        )
        context["q"] = query

        return context
