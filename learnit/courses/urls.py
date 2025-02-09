from django.urls import path

from .views import MainPage, CategoryPage, CoursePage, LessonPage, AuthorPage

urlpatterns = [
    path("", MainPage.as_view(), name="main"),
    path("<slug:category>", CategoryPage.as_view(), name="category"),
    path("course/<slug:course_slug>", CoursePage.as_view(), name="course"),
    path(
        "course/<slug:course_slug>/<int:lesson_order>",
        LessonPage.as_view(),
        name="lesson",
    ),
    path("author/<slug:author_id>", AuthorPage.as_view(), name="author"),
]
