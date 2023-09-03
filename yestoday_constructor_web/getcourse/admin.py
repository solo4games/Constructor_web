from django.contrib import admin

from .models import *


@admin.register(Audio)
class FilterAudio(admin.ModelAdmin):
    list_display = (
        "id",
        "text_up",
        "text_down",
        "seekbar",
        "src",
        "file",
    )


@admin.register(GetCourseUser)
class FilterGetCourseUser(admin.ModelAdmin):
    list_display = (
        "id",
        "accountUserId",
        "get_audios",
    )


@admin.register(Lesson)
class FilterLesson(admin.ModelAdmin):
    list_display = (
        "date_time",
    )


@admin.register(LessonBooked)
class FilterLessonBooked(admin.ModelAdmin):
    list_display = (
        "date_time",
        "teacher",
        "student",
        "zoom_id",
        "zoom_url",
        "zoom_password",
    )


@admin.register(GetCourseTeacher)
class FilterGetCourseTeacher(admin.ModelAdmin):
    list_display = (
        "user",
        "accountUserId",
    )


@admin.register(GetCourseStudent)
class FilterGetCourseStudent(admin.ModelAdmin):
    list_display = (
        "user",
        "teacher",
        "hours",
        "name",
        "surname",
        "email",
    )
