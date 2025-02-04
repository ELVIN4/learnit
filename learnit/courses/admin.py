from django.contrib import admin
from .models import Category, Course, Lesson, Language
from .forms.course_form import CourseAdminForm

admin.site.site_header = "LearnIT"


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug", 
        "category",
        "lessons_count",
        "priority",
        "author",
        "language",
        "is_published",
        "update_date",
        "upload_date",
    )
    search_fields = ["name", "slug", "category__name", "author", "language__name", "is_published"]
    ordering = ["update_date", "upload_date"]

    def get_form(self, request, obj = ..., change = ..., **kwargs):
        if not obj:
            kwargs['form'] = CourseAdminForm
            
        return super().get_form(request, obj, change, **kwargs)
    def get_fields(self, request, obj=...):
        if obj:
            return [
                "name",
                "slug",
                "thumbnail",
                "description",
                "url",
                "lessons_count",
                "author",
                "category",
                "total_views",
                "average_views",
                "total_duration",
                "language",
                "is_published",
                "priority"
            ]
        
        return super().get_fields(request, obj)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "priority", "create_date", "language", "is_published")
    search_fields = ("name", "slug", "language__name", "is_published")
    ordering = ("create_date",)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("name", "upload_date", "is_published", "course", "order")
    search_fields = ("name", "course__slug", "video_id", "is_published")
    ordering = ["course", "order"]


admin.site.register(
    [Language],
)
