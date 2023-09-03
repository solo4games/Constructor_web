import logging
import time
import requests
from datetime import datetime, timedelta


def main(now: datetime):
    if now.minute >= 20 and now.minute <= 30:
        requests.get(
            "https://yestoday.pythonanywhere.com/getcourse/send_notifications")
        requests.get(
            "https://yestoday.pythonanywhere.com/getcourse/delete_previous_zoom_meetings")
        next_time = now + timedelta(minutes=30)
        next_time = next_time.replace(minute=50, second=0, microsecond=0)

    elif now.minute >= 50 and now.minute < 60:
        requests.get(
            "https://yestoday.pythonanywhere.com/getcourse/send_notifications")
        requests.get(
            "https://yestoday.pythonanywhere.com/getcourse/delete_previous_zoom_meetings")
        next_time = now + timedelta(minutes=30)
        next_time = next_time.replace(minute=20, second=0, microsecond=0)

    elif now.minute < 20:
        next_time = now.replace(minute=20, second=0, microsecond=0)

    elif now.minute > 30 and now.minute < 50:
        next_time = now.replace(minute=50, second=0, microsecond=0)
    time_to_sleep = (next_time - now).seconds
    time.sleep(time_to_sleep)
    logging.info('done')
    return main(datetime.now())


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s %(message)s',
        # filename='notifications.log',
        encoding='utf-8',
        level=logging.INFO
    )
    now = datetime.now()
    logging.info('started')
    try:
        main(now)
    except Exception as err:
        logging.exception(err)
