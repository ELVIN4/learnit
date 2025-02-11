from django.urls import path

from .views import (
    MainPage,
    CategoryPage,
    CoursePage,
    LessonPage,
    AuthorPage,
    SearchPage,
    AllCategoriesPage,
)

urlpatterns = [
    path("", MainPage.as_view(), name="main"),
    path("search/", SearchPage.as_view(), name="search"),
    path("categories/", AllCategoriesPage.as_view(), name="categories"),
    path("<slug:category>", CategoryPage.as_view(), name="category"),
    path("course/<slug:course_slug>", CoursePage.as_view(), name="course"),
    path(
        "course/<slug:course_slug>/<int:lesson_order>",
        LessonPage.as_view(),
        name="lesson",
    ),
    path("author/<slug:author_id>", AuthorPage.as_view(), name="author"),
]
