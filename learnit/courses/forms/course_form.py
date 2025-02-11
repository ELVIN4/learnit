from django import forms
from django.forms import ValidationError
from courses.models import Course, Lesson
from datetime import datetime
from courses.services.yt_scrapper_v2 import get_playlist_info


class CourseAdminForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["category", "url", "is_published", "priority", "language"]

    def clean(self):
        cleaned_data = super().clean()
        url = cleaned_data.get("url")

        try:
            self.course = get_playlist_info(url)
        except Exception as e:
            raise ValidationError(e)

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit)
        course = self.course

        instance.name = course["playlist"]["title"]
        instance.thumbnail = course["playlist"]["thumbnail"]
        instance.description = course["playlist"]["description"]
        instance.lessons_count = course["playlist"]["video_count"]
        instance.total_views = course["playlist"]["total_views"]
        instance.average_views = course["playlist"]["average_views"]
        instance.total_duration = course["playlist"]["total_duration"]
        instance.author = course["playlist"]["author"]
        instance.author_id = course["playlist"]["author_id"]
        instance.modified_date = datetime.strptime(
            course["playlist"]["modified_date"], "%Y%m%d"
        )

        instance.save()

        for lesson in course["lessons"]:
            Lesson.objects.create(
                name=lesson["title"],
                description=lesson["description"],
                thumbnail=lesson["thumbnail"],
                views=lesson["views"],
                video_id=lesson["id"],
                duration=lesson["duration"],
                course=instance,
            )

        return instance
