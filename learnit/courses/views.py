from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Course, Category, Lesson


class MainPage(View):
    '''Главная страница курсов'''
    def get(self, request):
        courses = Course.objects.all()
        categories = Category.objects.all()

        return render(
            request,
            'courses/base.html',
            context={"courses": courses, "categories": categories},
        )

class CategoryPage(View):
    '''Вывод всех курсов по категории'''
    def get(self, request, category):
        category = get_object_or_404(Category.objects.all().filter(slug=category))
        child_categories = Category.objects.filter(parent_category=category)
        courses = Course.objects.all().filter(category=category)

        return render(
            request,
            'courses/index.html',
            context={'category':category, 'courses':courses, 'child_categories': child_categories,},
        )
    

class CoursePage(View):
    '''Вывод всех уроков по курсу'''
    def get(self, request, course_slug):
        course = get_object_or_404(Course.objects.filter(slug=course_slug))
        lessons = Lesson.objects.filter(course=course)

        return render(request, 'courses/course.html', context={'lessons':lessons, 'course':course})
    

class LessonPage(View):
    '''Урок'''
    def get(self, request, course_slug, lesson_order):
        lesson = get_object_or_404(Lesson.objects.filter(course__slug=course_slug, order=lesson_order))
        
        return render(
            request,
            'courses/lesson.html',
            context={'lesson':lesson}
        )