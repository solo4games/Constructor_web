from datetime import datetime
import requests
from .models import LessonBooked
from django.utils import timezone

from .services_getcourse import _delete_meeting

from yestoday_constructor_web.settings import SALEBOT_API_KEY


def send_notifications():
    now, time_remaining = _get_current_time()
    lessons_list = _get_nearest_lessons(now)
    print(lessons_list)

    for el in lessons_list:
        telegram_client_id = el.student.telegram_client_id
        if telegram_client_id:
            url = el.zoom_url
            _send_telegram_notification(
                telegram_client_id, url, time_remaining)


def delete_previous_zoom_meetings():
    for lesson in LessonBooked.objects.filter(
            date_time__lte=timezone.now()-timezone.timedelta(hours=2)):
        _delete_meeting(lesson.student, lesson)


def _get_current_time() -> datetime:
    now = timezone.now()
    if now.minute <= 30:
        time_remaining = 30 - now.minute
        now = now.replace(minute=30, second=0, microsecond=0)
    else:
        time_remaining = 60 - now.minute
        now = now.replace(hour=now.hour+1, minute=0, second=0, microsecond=0)

    return (now, time_remaining)


def _get_nearest_lessons(now: datetime) -> list:
    return [el for el in LessonBooked.objects.filter(date_time=now)]


def _send_telegram_notification(client_id: int, url: str, time_remaining: int) -> None:
    requests.post(
        f"https://chatter.salebot.pro/api/{SALEBOT_API_KEY}/message",
        json={
            "message": f"Через {time_remaining} минут стартует урок.\nМожете заходить в комнату, преподаватель вас ждёт",
            "client_id": client_id,

            "buttons": {
                "hint": f"{url}",
                        "buttons": [
                            {
                                "line": 0,
                                "index_in_line": 0,
                                "text": "Присоединиться",
                                "type": "inline",
                                "url": url
                            }
                        ]
            }
        }
    )
