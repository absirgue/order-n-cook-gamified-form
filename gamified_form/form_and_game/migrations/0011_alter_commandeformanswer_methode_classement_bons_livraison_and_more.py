# Generated by Django 4.1.5 on 2023-02-08 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('form_and_game', '0010_player_booked_phone_call'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commandeformanswer',
            name='methode_classement_bons_livraison',
            field=models.CharField(choices=[('classeur', 'Classeur'), ('trieur', 'Trieur'), ('ordinateur', 'Ordinateur'), ('comptabilite', 'envoi à la comptabilité en direct'), ('non gardées', '(je ne les garde pas)'), ('Autre', 'Autre')], max_length=90),
        ),
        migrations.AlterField(
            model_name='commandeformanswer',
            name='methode_classement_commandes',
            field=models.CharField(choices=[('classeur', 'Classeur'), ('trieur', 'Trieur'), ('ordinateur', 'Ordinateur'), ('comptabilite', 'envoi à la comptabilité en direct'), ('non gardées', '(je ne les garde pas)'), ('Autre', 'Autre')], max_length=90),
        ),
        migrations.CreateModel(
            name='CallDemand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='form_and_game.player')),
            ],
        ),
    ]