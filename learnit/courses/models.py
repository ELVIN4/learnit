from django.db import models


class Category(models.Model):
    parent_category = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=140)
    priority = models.IntegerField(default=0)
    create_date = models.DateTimeField(auto_now=True)
    language = models.ForeignKey("Language", on_delete=models.PROTECT)
    is_published = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(null=True)
    thumbnail = models.URLField(null=True)
    description = models.TextField(null=True)
    url = models.URLField(unique=True)
    lessons_count = models.IntegerField()
    author = models.CharField(max_length=200)
    author_id = models.CharField(null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    total_views = models.PositiveIntegerField(default=0)
    average_views = models.PositiveIntegerField(default=0)
    total_duration = models.PositiveIntegerField(default=0)

    language = models.ForeignKey("Language", on_delete=models.PROTECT)
    is_published = models.BooleanField(default=True)
    priority = models.IntegerField(default=0)
    upload_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)
    modified_date = models.DateField(null=True)

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=400)
    description = models.TextField(null=True)
    video_id = models.CharField(unique=False)
    thumbnail = models.URLField(default=None)
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    duration = models.PositiveIntegerField(default=0)
    upload_date = models.DateTimeField(auto_now_add=True)

    is_published = models.BooleanField(default=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(blank=True)

    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"
        ordering = ["order"]  # уроки будут сортироваться по полю "order"

    def save(self, *args, **kwargs):
        # если порядок не задан явно, ставим его автоматически
        if self.order is None:
            last_lesson = (
                Lesson.objects.filter(course=self.course).order_by("order").last()
            )
            self.order = (last_lesson.order + 1) if last_lesson else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Language(models.Model):
    """Языки курсов"""

    name = models.CharField(max_length=64)
    code = models.CharField(max_length=2)
    priority = models.IntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Languages"

    def __str__(self):
        return self.name
