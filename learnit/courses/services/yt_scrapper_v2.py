import yt_dlp


def get_playlist_info(playlist_url):
    ydl_opts = {
        "quiet": True,
        "extract_flat": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        playlist_info = ydl.extract_info(playlist_url, download=False)

        course = {
            "playlist": {
                "title": playlist_info["title"],
                "description": playlist_info.get("description", None),
                "thumbnail": playlist_info["thumbnails"][3]["url"],
                "author": playlist_info.get("uploader", None),
                "author_id": playlist_info.get("channel_id"),
                "video_count": len(playlist_info["entries"]),
                "modified_date": playlist_info.get("modified_date"),
                "total_views": 0,
                "average_views": 0,
                "total_duration": 0,
            },
            "lessons": [],
        }

        total_views = 0
        total_duration = 0

        for video in playlist_info["entries"]:
            lesson = {
                "id": video["id"],
                "channel": video["channel"],
                "description": video.get("description", None),
                "thumbnail": video["thumbnails"][3]["url"],
                "title": video["title"],
                "duration": video.get("duration", 0),
                "views": video.get("view_count", 0),
            }

            course["lessons"].append(lesson)
            total_duration += video.get("duration")
            total_views += video.get("view_count")

        course["playlist"]["total_views"] = total_views
        course["playlist"]["total_duration"] = total_duration
        course["playlist"]["average_views"] = total_views // len(
            playlist_info["entries"]
        )

    return course
