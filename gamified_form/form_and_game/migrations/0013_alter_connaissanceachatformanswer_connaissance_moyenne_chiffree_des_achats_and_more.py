# Generated by Django 4.1.5 on 2023-02-18 15:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_and_game', '0012_user_randomly_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connaissanceachatformanswer',
            name='connaissance_moyenne_chiffree_des_achats',
            field=models.CharField(choices=[('Par semaine', 'par semaine'), ('Par décade', 'par décade'), ('Par mois', 'par mois'), ('Autre', 'autre')], max_length=90),
        ),
        migrations.AlterField(
            model_name='connaissanceachatformanswer',
            name='gain_estime_si_ligne_a_ligne',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(limit_value=0)]),
        ),
    ]
