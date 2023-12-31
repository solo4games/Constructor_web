# Generated by Django 4.1 on 2022-08-18 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('getcourse', '0007_remove_getcoursestudent_lessons_lessonbooked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonbooked',
            name='password',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Пароль встречи'),
        ),
        migrations.AlterField(
            model_name='lessonbooked',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='getcourse.getcoursestudent', verbose_name='Ученик'),
        ),
        migrations.AlterField(
            model_name='lessonbooked',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='getcourse.getcourseteacher', verbose_name='Учитель'),
        ),
    ]
