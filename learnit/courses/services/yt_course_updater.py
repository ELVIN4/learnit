import logging
from django.db.models import QuerySet
from courses.models import Lesson
from .yt_scrapper_v2 import get_playlist_info

logger = logging.getLogger("celery")


def course_updater(courses: QuerySet):
    updated_count = 0
    error_count = 0

    for course in courses:
        try:
            info = get_playlist_info(playlist_url=course.url)
            course.name = info["playlist"]["title"]
            course.thumbnail = info["playlist"]["thumbnail"]
            course.description = info["playlist"]["description"]
            course.lessons_count = info["playlist"]["video_count"]
            course.total_views = info["playlist"]["total_views"]
            course.modified_date = info["playlist"]["modified_date"]
            course.average_views = info["playlist"]["average_views"]
            course.total_duration = info["playlist"]["total_duration"]

            _update_or_create_lessons(course, info["lessons"])

            course.save()
            updated_count += 1

        except Exception as e:
            logger.warning(f"course updater ERROR {e}")
            error_count += 1

    return f"Success {updated_count}, Errors {error_count}"


def _update_or_create_lessons(course, lessons_data):
    """
    update or create lessons for the course based on the transferred data
    """
    try:
        for lesson_data in lessons_data:
            lesson, created = Lesson.objects.update_or_create(
                course=course,
                video_id=lesson_data["id"],
                defaults={
                    "name": lesson_data["title"],
                    "description": lesson_data["description"],
                    "views": lesson_data["views"],
                    "thumbnail": lesson_data["thumbnail"],
                    "duration": lesson_data["duration"],
                },
            )
            if created:
                logger.info(
                    f"created new lesson {lesson.name} for course {course.name}"
                )

    except Exception as e:
        logging.warning(f"lesson update/create ERROR {e}")
