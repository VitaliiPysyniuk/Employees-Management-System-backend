# Generated by Django 4.1.1 on 2022-11-25 11:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quizzes', '0005_remove_quizresultmodel_employee'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizresultmodel',
            name='employee',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='passed_quizzes', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
