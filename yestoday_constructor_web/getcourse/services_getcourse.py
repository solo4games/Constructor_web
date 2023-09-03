import traceback
from datetime import datetime
import logging
from typing import Optional
from uuid import UUID
from .models import Answer, Audio, GetCourseUser, GetCourseStudent, GetCourseTeacher, Lesson, LessonBooked
from django.utils import timezone

from django_zoom_meetings import ZoomMeetings

logger = logging.getLogger(__name__)


def add_audio_to_getcourse_user_dict(user_id: int, audio_id: int):
    audio = _get_audio(audio_id)
    if audio:
        _get_or_create_getcourse_user(user_id).audios.add(audio)
        return True
    return False


def delete_audio_from_getcourse_user_dict(user_id: int, audio_id: int):
    audio = _get_audio(audio_id)
    if audio:
        _get_or_create_getcourse_user(user_id).audios.remove(audio)
        return True
    return False


def get_audio_ids_from_getcourse_user_dict(user_id: int):
    return [el.id for el in _get_or_create_getcourse_user(user_id).audios.all()]


def show_getcourse_user_dict(user_id: int):
    return "\n".join([el.to_html() for el in _get_or_create_getcourse_user(user_id).audios.all()])


def add_student(
    user_id: int,
    name: str,
    surname: str,
    email: str,
    teacher_id: int,
    hours: float
) -> bool:
    user = _get_or_create_getcourse_user(user_id)
    teacher = _get_getcourse_teacher(teacher_id)

    if not teacher:
        return False

    return bool(
        _get_or_create_getcourse_student(
            user,
            teacher,
            name=name,
            surname=surname,
            email=email,
            hours=hours
        )
    )


def book_lesson(
    user_id: int,
    date_time: datetime
) -> dict:
    if date_time <= timezone.now():
        return {"status": "ERROR", "msg": "Нельзя записаться на прошедшее время"}
    student = _get_getcourse_student(user_id=user_id)
    if not student:
        return {"status": "ERROR", "msg": "Вы не зарегестрированы в системе"}

    if not _student_has_payed_hours(student):
        return {"status": "ERROR", "msg": "У вас больше нет доступных уроков"}

    if _student_booked_more_than_four_lessons_per_day(student, date_time):
        return {"status": "ERROR", "msg": "Доступно не более 4 записей в день"}

    if _student_has_lesson_at_this_time(date_time, student):
        return {"status": "ERROR", "msg": "Уже есть запись на это время"}

    try:
        lesson = _get_lesson_from_teacher(date_time, student.teacher)
    except Lesson.DoesNotExist:
        return {"status": "ERROR", "msg": "Выбранное время недоступно для бронирования"}

    return _book_lesson(student, lesson)


def unbook_lesson(
    user_id: int,
    date_time: datetime
) -> dict:
    if date_time - timezone.timedelta(hours=12) <= timezone.now():
        return {"status": "ERROR", "msg": "Нельзя отменить урок менее, чем за 12 часов"}
    student = _get_getcourse_student(user_id=user_id)
    if not student:
        return {"status": "ERROR", "msg": "Вы не зарегестрированы в системе"}

    try:
        lesson = _get_lesson_from_student(date_time, student)
    except Lesson.DoesNotExist:
        return {"status": "ERROR", "msg": "У вас нет забронированного урока в это время"}

    return _unbook_lesson(student, lesson)


def book_lesson_teacher(
    user_id: int,
    date_time: datetime
) -> dict:
    if date_time <= timezone.now():
        return {"status": "ERROR", "msg": "Нельзя создать урок на прошедшее время"}
    teacher = _get_getcourse_teacher(teacher_id=user_id)
    if not teacher:
        return {"status": "ERROR", "msg": "Вы не зарегестрированы в системе"}

    lesson = _get_or_create_lesson(date_time=date_time)

    _book_lesson_teacher(teacher=teacher, lesson=lesson)

    return {"status": "OK", "msg": "Урок создан"}


def unbook_lesson_teacher(
    user_id: int,
    date_time: datetime
) -> dict:
    if date_time <= timezone.now() + timezone.timedelta(days=7):
        return {"status": "ERROR", "msg": "Нельзя отменять уроки на ближайшие 7 дней"}

    teacher = _get_getcourse_teacher(teacher_id=user_id)
    if not teacher:
        return {"status": "ERROR", "msg": "Вы не зарегестрированы в системе"}

    if _any_student_has_lesson_at_this_time(date_time, teacher):
        return {"status": "ERROR", "msg": "Ученик уже записан на это время"}

    try:
        lesson = _get_lesson_from_teacher(date_time, teacher)
    except Lesson.DoesNotExist:
        return {"status": "ERROR", "msg": "У вас нет забронированного урока в это время"}

    _unbook_lesson_teacher(teacher, lesson)

    return {"status": "OK", "msg": "Урок отменен"}


def get_lessons(user_id: int) -> list:
    student = _get_getcourse_student(user_id)
    if not student:
        return {"status": "ERROR", "msg": "Вы не зарегестрированы в системе"}

    return {"status": "OK", "result": student.get_lessons_list()}


def get_lessons_today(user_id: int, date_time: datetime) -> list:
    student = _get_getcourse_student(user_id)

    if not student:
        return {"status": "ERROR", "msg": "Вы не зарегестрированы в системе"}

    return {"status": "OK", "result": student.get_lessons_list_for_date_time(date_time=date_time)}


def get_available_lessons_teacher_by_student(user_id: int) -> list:
    student = _get_getcourse_student(user_id)
    if not student:
        return {"status": "ERROR", "msg": "Вы не зарегестрированы в системе"}
    response = _get_available_lessons_teacher(student.teacher.accountUserId)
    if response.get('status') != 'OK':
        return {"status": "ERROR", "msg": "Произошла ошибка"}

    return response


def get_available_lessons_teacher(user_id: int) -> list:
    teacher = _get_getcourse_teacher(user_id)
    if not teacher:
        return {"status": "ERROR", "msg": "Вы не зарегестрированы в системе"}
    response = _get_available_lessons_teacher(teacher.accountUserId)
    if response.get('status') != 'OK':
        return {"status": "ERROR", "msg": "Произошла ошибка"}

    return response


def get_lessons_teacher(user_id: int) -> list:
    teacher = _get_getcourse_teacher(user_id)
    if not teacher:
        return {"status": "ERROR", "msg": "Вы не зарегестрированы в системе"}

    return {
        "status": "OK",
        "result":
            [
                {
                    'student': str(st),
                    'lessons': st.get_lessons_list()
                } for st in _get_students_of_teacher(teacher=teacher)
            ]
    }


def get_lessons_today_teacher(user_id: int, date_time: datetime) -> list:
    teacher = _get_getcourse_teacher(user_id)
    if not teacher:
        return {"status": "ERROR", "msg": "Вы не зарегестрированы в системе"}

    return {
        "status": "OK",
        "result":
            [
                {
                    'student': str(st),
                    'lessons': st.get_lessons_list_for_date_time(date_time)
                } for st in _get_students_of_teacher(teacher=teacher)
            ]
    }


def get_info_for_student(user_id: int) -> dict:
    student = _get_getcourse_student(user_id=user_id)
    if not student:
        return {"status": "ERROR", "msg": "Вы не зарегестрированы в системе"}

    return {
        'status': 'OK',
        'hours': student.hours,
        'teacherName': student.teacher.user.first_name + ' ' + student.teacher.user.last_name,
        'teacherPhoto': student.teacher.photo,
        'isSub': bool(student.telegram_client_id),
    }


def add_notifications_to_student(user_id, telegram_client_id) -> dict:
    student = _get_getcourse_student(user_id=user_id)
    if not student:
        return {"status": "ERROR", "msg": "Вы не зарегестрированы в системе"}

    student.telegram_client_id = telegram_client_id

    student.save()

    return {"status": "OK", "msg": "Отлично, теперь вы будете получать уведомления об уроках"}


def _get_available_lessons_teacher(user_id: int) -> list:
    teacher = _get_getcourse_teacher(user_id)
    if not teacher:
        return {"status": "ERROR", "msg": "Вы не зарегестрированы в системе"}

    return {"status": "OK", "result": [str(el) for el in teacher.available_lessons.all()]}


def _get_students_of_teacher(teacher: GetCourseTeacher) -> list:
    return GetCourseStudent.objects.filter(teacher=teacher)


def _book_lesson(student: GetCourseStudent, lesson: Lesson) -> None:

    response = _create_meeting(student, lesson)
    if response['status'] != 'OK':
        return response

    meeting = response['meeting']

    try:
        student.teacher.available_lessons.remove(lesson)
        student.lessons.create(
            date_time=lesson.date_time,
            teacher=student.teacher,
            student=student,
            zoom_url=meeting['join_url'],
            zoom_password=meeting['password'],
            zoom_id=meeting['id']
        )
        student.hours -= 0.5
        student.save()
    except Exception as err:
        print(f'err -> {err}')
        return {"status": "ERROR", "msg": "Произошла ошибка, попробуйте еще раз или обратитесь в поддержку"}

    return {"status": "OK", "msg": "Урок забронирован"}


def _unbook_lesson(student: GetCourseStudent, lesson: LessonBooked) -> None:
    meeting = _delete_meeting(student, lesson)
    if meeting['status'] != 'OK':
        return meeting

    try:
        student.teacher.available_lessons.add(
            Lesson.objects.get_or_create(
                date_time=lesson.date_time
            )[0]
        )
        student.lessons.filter(date_time=lesson.date_time).delete()
    except Exception as err:
        print(f"err -> {err}")
        traceback.print_exc()
        return {"status": "ERROR", "msg": "Произошла ошибка, попробуйте еще раз или обратитесь в поддержку"}

    return {"status": "OK", "msg": "Бронь отменена"}


def _create_meeting(student: GetCourseStudent, lesson: Lesson):
    try:
        my_zoom = ZoomMeetings(
            student.teacher.zoom_key,
            student.teacher.zoom_sec,
            student.teacher.zoom_email
        )
        try:
            my_zoom.request_token = my_zoom.request_token.decode('utf-8')
        except AttributeError:
            pass
        meeting = my_zoom.CreateMeeting(
            date=lesson.date_time,
            topic=f"Урок с {student.name} {student.surname}",
            meeting_duration=30,
            meeting_password=student.user.accountUserId
        )
    except Exception as err:
        print(f'err -> {err}')
        return {'status': 'ERROR', 'msg': 'Не удалось создать встречу Zoom'}

    return {'status': 'OK', 'meeting': meeting}


def _delete_meeting(student: GetCourseStudent, lesson: LessonBooked):
    try:
        my_zoom = ZoomMeetings(
            student.teacher.zoom_key,
            student.teacher.zoom_sec,
            student.teacher.zoom_email
        )
        try:
            my_zoom.request_token = my_zoom.request_token.decode('utf-8')
        except AttributeError:
            pass
        response = my_zoom.DeletMeeting(
            lesson.zoom_id
        )
        if response.status_code == 200:
            lesson.zoom_id = None
            lesson.zoom_password = None
            lesson.zoom_url = None
            lesson.save()
    except Exception as err:
        print(f'err -> {err}')
        return {'status': 'ERROR', 'msg': 'Не удалось удалить встречу Zoom'}
    return {'status': 'OK'}


def _book_lesson_teacher(teacher: GetCourseTeacher, lesson: Lesson) -> None:
    teacher.available_lessons.add(lesson)


def _unbook_lesson_teacher(teacher: GetCourseTeacher, lesson: Lesson) -> None:
    teacher.available_lessons.remove(lesson)


def _get_lesson_from_teacher(date_time: datetime, teacher: GetCourseTeacher) -> Lesson:

    return teacher.available_lessons.get(
        date_time=date_time
    )


def _get_lesson_from_student(date_time: datetime, student: GetCourseStudent) -> Lesson:

    return student.lessons.get(
        date_time=date_time
    )


def _student_has_lesson_at_this_time(
        date_time: datetime,
        student: GetCourseStudent
) -> bool:

    return student.lessons.check(
        date_time=date_time
    )


def _any_student_has_lesson_at_this_time(
        date_time: datetime,
        teacher: GetCourseTeacher
) -> bool:

    return any(
        [
            _student_has_lesson_at_this_time(date_time=date_time, student=st) for st in GetCourseStudent.objects.filter(
                teacher=teacher,
            )
        ]
    )


def _student_has_payed_hours(
    student: GetCourseStudent
) -> bool:
    return student.hours > 0


def _student_booked_more_than_four_lessons_per_day(
    student: GetCourseStudent,
    date_time: datetime
) -> bool:
    return student.lessons.filter(
        date_time__date=date_time.date()
    ).count() >= 4


def _get_or_create_getcourse_student(
        user: GetCourseUser,
        teacher: GetCourseTeacher = None,
        name: str = None,
        surname: str = None,
        email: str = None,
        hours: float = 0) -> GetCourseStudent:
    student, created = GetCourseStudent.objects.get_or_create(
        user=user,
        teacher=teacher,
        name=name,
        surname=surname,
        email=email,
        hours=hours
    )
    return student


def _get_getcourse_student(
    user_id: int,
) -> GetCourseStudent:
    try:
        student = GetCourseStudent.objects.get(
            user__accountUserId=user_id
        )
    except GetCourseStudent.DoesNotExist:
        return None

    return student


def _get_getcourse_teacher(teacher_id: int) -> GetCourseTeacher:
    try:
        teacher = GetCourseTeacher.objects.get(
            accountUserId=teacher_id
        )
    except GetCourseTeacher.DoesNotExist:
        return None

    return teacher


def _get_or_create_getcourse_user(user_id: int) -> GetCourseUser:
    user, created = GetCourseUser.objects.get_or_create(accountUserId=user_id)
    return user


def _get_or_create_lesson(date_time: datetime) -> Lesson:
    lesson, created = Lesson.objects.get_or_create(date_time=date_time)
    return lesson


def _get_audio(audio_id: int) -> list:
    return Audio.objects.get(pk=audio_id)


def register_answer(user_id: int, quiz_id: UUID, answer: dict):
    user = _get_or_create_getcourse_user(user_id)

    answer, _ = Answer.objects.get_or_create(
        quiz_id=quiz_id,
        answer=answer,
    )

    answer.users.add(user)

    return True


def get_answers(user_id: int, quiz_ids: list[UUID]) -> list[dict]:
    user = _get_or_create_getcourse_user(user_id)

    answers = Answer.objects.filter(
        users__id__exact=user.id,
        quiz_id__in=quiz_ids,
    ).all()

    return [{"quiz_id": answer.quiz_id, "answer": answer.answer} for answer in answers]


def delete_answers(user_id: int, quiz_ids: list[UUID]) -> list[dict]:
    user = _get_or_create_getcourse_user(user_id)

    answers = Answer.objects.filter(
        users__id__exact=user.id,
        quiz_id__in=quiz_ids,
    ).all()

    [answer.users.remove(user) for answer in answers]

    return True
