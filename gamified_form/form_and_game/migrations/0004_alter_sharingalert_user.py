# Generated by Django 4.1.5 on 2023-02-04 17:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_and_game', '0003_remove_sharingalert_user_sharingalert_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sharingalert',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]