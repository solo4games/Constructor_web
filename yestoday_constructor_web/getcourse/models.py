from datetime import datetime
from typing import Any, Dict, Tuple
from django.db import models
from django.core.files.base import ContentFile
from yestoday_constructor_web.settings import ALLOWED_HOSTS
import requests
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models.signals import post_delete
from django.dispatch import receiver


User = get_user_model()


class Audio(models.Model):
    text_up = models.CharField(
        'Текст сверху',
        max_length=500,
        blank=True,
        null=True
    )
    text_down = models.CharField(
        'Текст сверху',
        max_length=500,
        blank=True,
        null=True
    )
    seekbar = models.BooleanField('Доавить шкалу времени', default=False)
    src = models.CharField('Ссылка на источник',
                           max_length=500, blank=True, null=True)
    file = models.FileField('Файл', upload_to='audio', blank=True, null=True)

    class Meta:
        verbose_name = "Аудио"
        verbose_name_plural = "Аудио"

    def __str__(self) -> str:
        return f"{self.text_up}, {self.text_down}"[:50] + '...'

    def save(self, *args, **kwargs) -> None:
        if 'api.voicerss.org' in self.src:
            r = requests.get(self.src)
            new_id = Audio.objects.latest('id').id + 1
            self.file = ContentFile(r.content, f"{new_id}.mp3")
        return super().save(*args, **kwargs)

    def to_html(self) -> str:

        if self.seekbar:
            seekbar = """
        <div>
                    <progress class="podcast-progress" id='podcast-progress' value="0" max="1"
                        onclick="audioTimeLineClick(this, event)"></progress>
                    <div class="f-container" id='f-container'>
                        <div class="podcast-time" id='podcast-time'>00:00 / 00:00</div>
                        <div class="podcast-speed" id='podcast-speed'>
                            <a class="podcast-speed-10 active" href="javascript:void(0)"
                                onclick="audioChangeSpeedClick(this)">1x</a> / <a class="podcast-speed-15"
                                href="javascript:void(0)" onclick="audioChangeSpeedClick(this)">1.5x</a> / <a
                                class="podcast-speed-20" href="javascript:void(0)"
                                onclick="audioChangeSpeedClick(this)">2x</a>
                        </div>
                    </div>
                </div>
        """
        else:
            seekbar = ""

        return f"""
        <div class='audio-tts{self.id} audio-div' id='audio-tts'>
                <audio class="audio-player{self.id}" id='audio-player' src="{'https://'+ ALLOWED_HOSTS[0] + self.file.url if 'api.voicerss.org' in self.src else self.src}"
                    onended="audioOnEnded(this)" oncanplay="audioOnCanPlay(this)" onplay="audioPlay(this)"
                    onpause="audioPause(this)"></audio>
                <div class="podcast-container" id='podcast-container'>
                    <div class="h-container" id='h-container'>
                        <div class="podcast-playpause" id='podcast-playpause'>
                            <img class="play" id="play"
                                src="https://fs.getcourse.ru/fileservice/file/download/a/44237/sc/337/h/cb28b80bb66ad56d3c12fd1885bc3ef8.svg"
                                onclick="playPauseClick(this)">
                            <img class="pause" id="pause"
                                src="https://fs.getcourse.ru/fileservice/file/download/a/44237/sc/197/h/7395c5433ab34099a1d5b9b139efdd5b.svg"
                                onclick="playPauseClick(this)">
                        </div>
                        <div>
                            <div class="podcast-title" id='podcast-title'>{self.text_up}
                            <button type="button" onclick="audioSaveBtnClick(this)" id="{self.id}"><i
                                    class="bi bi-bookmark-star-fill active"></i></button></div>
                            <div class="podcast-subtitle" id='podcast-subtitle'>{self.text_down}</div>
                        </div>
                    </div>

                </div>
                {seekbar}

            </div>
            """


class Lesson(models.Model):
    date_time = models.DateTimeField('Дата и время урока')

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self) -> str:
        return str(self.date_time)


class GetCourseTeacher(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Логин пользователя"
    )
    accountUserId = models.BigIntegerField(
        'ID с GetCourse',
        unique=True,
    )

    available_lessons = models.ManyToManyField(
        Lesson,
        verbose_name='Доступные уроки',
        blank=True
    )

    photo = models.URLField(
        'Фото профиля',
        default='https://myyestoday.ru/public/img/default_profile_50.png'
    )

    zoom_key = models.CharField('Ключ Zoom', max_length=500)
    zoom_sec = models.CharField('Секретный ключ Zoom', max_length=500)
    zoom_email = models.EmailField('Почта Zoom')

    class Meta:
        verbose_name = "Учитель GetCourse"
        verbose_name_plural = "Учителя GetCourse"

    def __str__(self) -> str:
        return f"{self.accountUserId} {self.user.first_name} {self.user.last_name}"


class GetCourseUser(models.Model):
    accountUserId = models.BigIntegerField(
        'ID с GetCourse',
        unique=True,
    )
    audios = models.ManyToManyField(
        Audio,
        verbose_name='Аудио'
    )

    class Meta:
        verbose_name = "Пользователь GetCourse"
        verbose_name_plural = "Пользователи GetCourse"

    def get_audios(self):
        return "\n".join([str(p) for p in self.audios.all()])

    def __str__(self) -> str:
        return str(self.accountUserId)


class GetCourseStudent(models.Model):
    user = models.OneToOneField(
        GetCourseUser,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )

    teacher = models.ForeignKey(
        GetCourseTeacher,
        on_delete=models.CASCADE,
        verbose_name="Учитель",
        blank=True,
        null=True
    )

    # lessons = models.ManyToManyField(
    #     LessonBooked,
    #     verbose_name='Уроки',
    #     blank=True
    # )

    hours = models.FloatField(
        'Куплено часов',
        blank=True,
        null=True
    )

    name = models.CharField(
        'Имя',
        max_length=500,
        blank=True,
        null=True
    )

    surname = models.CharField(
        'Фамилия',
        max_length=500,
        blank=True,
        null=True
    )
    email = models.EmailField(
        'Почта',
        blank=True,
        null=True
    )

    telegram_client_id = models.CharField(
        "ID Salebot",
        max_length=500,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Ученик GetCourse"
        verbose_name_plural = "Ученики GetCourse"

    def get_lessons(self):
        return "\n".join([str(p) for p in self.lessons.all()])

    def get_lessons_list(self):
        return [
            {
                "date": str(p),
                "url": p.zoom_url
            }
            for p in self.lessons.all()
        ]

    def get_lessons_list_for_date_time(self, date_time: datetime):
        return [str(p) for p in self.lessons.filter(date_time__date=date_time.date())]

    def __str__(self) -> str:
        return f"{self.user.__str__()} {self.name} {self.surname}"


class LessonBooked(models.Model):
    date_time = models.DateTimeField('Дата и время урока')
    teacher = models.ForeignKey(
        GetCourseTeacher,
        verbose_name='Учитель',
        on_delete=models.CASCADE,
        related_name='lessons'
    )

    student = models.ForeignKey(
        GetCourseStudent,
        verbose_name='Ученик',
        on_delete=models.CASCADE,
        related_name='lessons'
    )

    zoom_id = models.CharField(
        'ID встречи',
        blank=True,
        null=True,
        max_length=50
    )
    zoom_url = models.URLField('Ссылка на встречу', blank=True, null=True)
    zoom_password = models.CharField(
        'Пароль встречи',
        max_length=20,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Урок забронированный"
        verbose_name_plural = "Уроки забронированные"

    def __str__(self) -> str:
        return str(self.date_time)

    # def delete(self, using: Any = ..., keep_parents: bool = ...) -> Tuple[int, Dict[str, int]]:
    #     print(f'1 {self.student.hours=}')
    #     self.student.hours += 0.5
    #     self.student.save()
    #     print(f'2 {self.student.hours=}')

    #     return super().delete(using, keep_parents)


@receiver(post_delete, sender=LessonBooked)
def add_hours(sender, instance, **kwargs):
    print(f"{sender=}")
    instance.student.hours += 0.5
    instance.student.save()


class Answer(models.Model):
    users = models.ManyToManyField(
        GetCourseUser,
        verbose_name="Пользователь",
        blank=True,
    )

    quiz_id = models.UUIDField('№ задания')

    answer = models.JSONField('Ответ')

    def __str__(self):
        return f"{self.quiz_id} {self.answer}"

    class Meta:
        verbose_name = "Ответ ученика"
        verbose_name_plural = "Ответы учеников"
