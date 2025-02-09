import yt_dlp
from courses.models import Course, Lesson  # Импортируем модели


# Функция для извлечения информации о видео
def fetch_video_info(video_url):
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        video_info = ydl.extract_info(video_url, download=False)
        return video_info


# Функция для обработки видео
def process_video(video_url, video_number, total_videos, course):
    try:
        video_info = fetch_video_info(video_url)
        if video_info:
            video_id = video_info["id"]
            video_views = video_info.get("view_count", 0)
            video_likes = video_info.get("like_count", 0)
            video_date = video_info.get("upload_date")
            video_thumbnail = video_info.get("thumbnail", "https://fuck.com/")
            video_description = video_info.get("description", "")
            video_author = video_info.get("uploader", "Неизвестный")

            # Сохраняем видео как урок в базе данных
            lesson = Lesson(
                name=video_info["title"],
                description=video_description,
                author=video_author,
                video_id=video_id,
                thumbnail=video_thumbnail,
                views=video_views,
                likes=video_likes,
                upload_date=video_date,
                course=course,
                order=video_number,
            )
            lesson.save()  # Сохраняем урок в базу
            print(f"Сохранен урок: {lesson.name}")
    except Exception as e:
        print(f"Ошибка при обработке {video_url}: {e}")


# Основная функция для обработки плейлиста
def get_playlist_info(playlist_url):
    ydl_opts = {
        "extract_flat": True,  # Извлекаем только информацию, не загружаем видео
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        playlist_info = ydl.extract_info(playlist_url, download=False)

        playlist_title = playlist_info.get("title", "Без названия")
        playlist_description = playlist_info.get("description", "")
        playlist_thumbnail = playlist_info.get("thumbnail", "https://fuck.com/")
        playlist_author = playlist_info.get("uploader", "Неизвестный")

        # Создаем или обновляем запись курса
        course, created = Course.objects.update_or_create(
            url=playlist_url,
            defaults={
                "name": playlist_title,
                "description": playlist_description,
                "thumbnail": playlist_thumbnail,
                "slug": None,
                "lessons_count": len(playlist_info["entries"]),
                "author": playlist_author,
                "category": None,  # Установите категорию, если нужно
            },
        )
        print(f"Курс {'создан' if created else 'обновлен'}: {course.name}")

        if "entries" not in playlist_info:
            print("Не удалось извлечь данные плейлиста.")
            return

        total_videos = len(
            playlist_info["entries"]
        )  # Общее количество видео в плейлисте
        print(f"Всего видео в плейлисте: {total_videos}")

        # Обрабатываем каждое видео
        for idx, video in enumerate(playlist_info["entries"], start=1):
            video_url = f"https://www.youtube.com/watch?v={video['id']}"
            process_video(video_url, idx, total_videos, course)


# Запуск программы
