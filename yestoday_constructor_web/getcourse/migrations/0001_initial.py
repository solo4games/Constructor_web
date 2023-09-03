# Generated by Django 3.2.3 on 2022-07-17 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_up', models.CharField(blank=True, max_length=255, null=True, verbose_name='Текст сверху')),
                ('text_down', models.CharField(blank=True, max_length=255, null=True, verbose_name='Текст сверху')),
                ('seekbar', models.BooleanField(default=False, verbose_name='Доавить шкалу времени')),
                ('src', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ссылка на источник')),
                ('file', models.FileField(blank=True, null=True, upload_to='audio', verbose_name='Файл')),
            ],
            options={
                'verbose_name': 'Аудио',
                'verbose_name_plural': 'Аудио',
            },
        ),
        migrations.CreateModel(
            name='GetCourseUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accountUserId', models.BigIntegerField(verbose_name='ID с GetCourse')),
                ('audios', models.ManyToManyField(to='getcourse.Audio', verbose_name='Аудио')),
            ],
            options={
                'verbose_name': 'Пользователь GetCourse',
                'verbose_name_plural': 'Пользователи GetCourse',
            },
        ),
    ]
