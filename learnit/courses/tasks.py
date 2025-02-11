from celery import Celery
from .services.yt_course_updater import course_updater
from .models import Course

app = Celery("learnit")


@app.task
def all_courses_updater():
    queryset = Course.objects.all()
    print(course_updater(queryset))
