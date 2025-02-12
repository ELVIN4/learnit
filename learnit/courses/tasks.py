import logging
from celery import Celery
from .services.yt_course_updater import course_updater
from .models import Course

app = Celery("learnit")
logger = logging.getLogger("celery")


@app.task
def all_courses_updater():
    logger.info("start all_courses_updater task")
    queryset = Course.objects.all()
    logger.info(course_updater(queryset))
