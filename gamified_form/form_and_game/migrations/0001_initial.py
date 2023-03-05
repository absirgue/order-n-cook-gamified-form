# Generated by Django 4.1.5 on 2023-03-05 12:51

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import form_and_game.models
import form_and_game.user_manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('reset_password_token', models.CharField(blank=True, max_length=100)),
                ('accepted_conditions', models.BooleanField(default=False)),
                ('sharing_code', models.CharField(max_length=20)),
                ('randomly_created', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', form_and_game.user_manager.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('phone_number', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(code='invalid_phone_number', message='Phone number should be  8 or 13 digits long and can optionally be preceded by the country code followed by a space or a coma.', regex='/^(?:[0-8]\\d|9[0-8])\\d{3}$/')])),
                ('restaurant_name', models.CharField(blank=True, max_length=100)),
                ('checking_picture', models.FileField(blank=True, upload_to=form_and_game.models.player_directory_path)),
                ('to_contact_when_product_is_out', models.BooleanField(default=False)),
                ('points', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(limit_value=0)])),
                ('is_validated', models.BooleanField(default=False)),
                ('needs_precising', models.BooleanField(default=True)),
                ('was_added_precision_points', models.BooleanField(default=False)),
                ('booked_phone_call', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='SharingAlert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=100)),
                ('was_shared', models.BooleanField(default=False)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RecetteFormAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('support_memorisation', models.CharField(choices=[('sur du papier volant', 'sur du papier volant'), ('Sur un carnet', 'sur un carnet'), ('Excel ou autre tableur', 'sur Excel ou un autre tableur'), ('Word ou autre éditeur', 'sur Word ou autre éditeur'), ('Autre outil informatique', 'grâce à un autre outil informatique'), ('Autre', 'autre')], max_length=90)),
                ('satisfait_support_memorisation', models.CharField(choices=[('oui', 'oui'), ('non', 'non')], max_length=90)),
                ('temps_passe_minute_par_recette', models.IntegerField(validators=[django.core.validators.MinValueValidator(limit_value=0)])),
                ('est_ce_trop', models.CharField(choices=[('oui', 'oui'), ('non', 'non')], max_length=90)),
                ('methode_transmission_savoir', models.CharField(choices=[('Oralement', 'oralement'), ('Sur papier volant', 'sur papier volant'), ('Dans un classeur', "à l'aide de classeurs"), ('Autre', 'autre')], max_length=90)),
                ('satisfait_mode_transmission', models.CharField(choices=[('oui', 'oui'), ('non', 'non')], max_length=90)),
                ('player', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='form_and_game.player')),
            ],
        ),
        migrations.CreateModel(
            name='GeneralIntroductionFormAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metier', models.CharField(choices=[('Chef de cuisine et pâtissier propriétaire', 'chef de cuisine et pâtissier propriétaire'), ('Chef de cuisine et pâtissier salarié actionnaire', 'chef de cuisine et pâtissier salarié actionnaire'), ('Chef de cuisine et pâtissier salarié', 'chef de cuisine et pâtissier salarié')], max_length=90)),
                ('ville', models.CharField(max_length=35)),
                ('age', models.IntegerField(validators=[django.core.validators.MinValueValidator(limit_value=0)])),
                ('experience', models.IntegerField(validators=[django.core.validators.MinValueValidator(limit_value=0)])),
                ('nombre_couverts', models.IntegerField(validators=[django.core.validators.MinValueValidator(limit_value=0)])),
                ('nombre_places', models.IntegerField(validators=[django.core.validators.MinValueValidator(limit_value=0)])),
                ('nombre_cuisiniers', models.IntegerField(validators=[django.core.validators.MinValueValidator(limit_value=0)])),
                ('prix_moyen_couvert', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(limit_value=0)])),
                ('nombre_etablissements', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(limit_value=1)])),
                ('player', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='form_and_game.player')),
            ],
        ),
        migrations.CreateModel(
            name='FonctionnalitesPrefereesFormAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('premiere_fonctionnalite', models.CharField(choices=[('Gestion des Commandes et Catalogues fournisseurs', 'Gestion des Commandes et Catalogues fournisseurs'), ('Gestion de la réception des Commandes et des Avoirs', 'Gestion de la réception des Commandes et des Avoirs'), ("Outil d'écriture et de stockage des recettes avec capacité de les partager aux membres de la cuisine ", "Outil d'écriture et de stockage des recettes avec capacité de les partager aux membres de la cuisine "), ('Scan intelligent des bons de réception/factures pour automatiser leur analyse ligne à ligne', 'Scan intelligent des bons de réception/factures pour automatiser leur analyse ligne à ligne'), ('Accès en temps réel à des données sur la masse et la répartition sur plusieurs critères des dépenses matière', 'Accès en temps réel à des données sur la masse et la répartition sur plusieurs critères des dépenses matière'), ('Calculateur intelligent de votre marge et de votre coefficient', 'Calculateur intelligent de votre marge et de votre coefficient'), ("Calculateur du coût total d'une recette en se basant sur le salaire horaire moyen", "Calculateur du coût total d'une recette en se basant sur le salaire horaire moyen"), ("Suivi et alerte en temps réel et depuis votre mobile de la rentabilité d'une recette", "Suivi et alerte en temps réel et depuis votre mobile de la rentabilité d'une recette"), ("Aide au calcul du bon prix de vente d'une recette", "Aide au calcul du bon prix de vente d'une recette"), ('Aide à la créativité en proposant une interface indiquant les produits de saison', 'Aide à la créativité en proposant une interface indiquant les produits de saison'), ("Capacité à suivre l'évolution des prix d'un produit sur l'année", "Capacité à suivre l'évolution des prix d'un produit sur l'année"), ("Création d'une interface pour les clients permettant de consulter les allergènes et l'origine des produits d'une recette", "Création d'une interface pour les clients permettant de consulter les allergènes et l'origine des produits d'une recette"), ("Aide à la réalisation d'un inventaire", "Aide à la réalisation d'un inventaire"), ("Aide au respect des règles d'hygiène", "Aide au respect des règles d'hygiène"), ('Prémunission au turnover en sauvegardant vos recette, transmission du savoir', 'Prémunission au turnover en sauvegardant vos recette, transmission du savoir'), ('Gestion du linge', 'Gestion du linge')], max_length=125)),
                ('deuxieme_fonctionnalite', models.CharField(choices=[('Gestion des Commandes et Catalogues fournisseurs', 'Gestion des Commandes et Catalogues fournisseurs'), ('Gestion de la réception des Commandes et des Avoirs', 'Gestion de la réception des Commandes et des Avoirs'), ("Outil d'écriture et de stockage des recettes avec capacité de les partager aux membres de la cuisine ", "Outil d'écriture et de stockage des recettes avec capacité de les partager aux membres de la cuisine "), ('Scan intelligent des bons de réception/factures pour automatiser leur analyse ligne à ligne', 'Scan intelligent des bons de réception/factures pour automatiser leur analyse ligne à ligne'), ('Accès en temps réel à des données sur la masse et la répartition sur plusieurs critères des dépenses matière', 'Accès en temps réel à des données sur la masse et la répartition sur plusieurs critères des dépenses matière'), ('Calculateur intelligent de votre marge et de votre coefficient', 'Calculateur intelligent de votre marge et de votre coefficient'), ("Calculateur du coût total d'une recette en se basant sur le salaire horaire moyen", "Calculateur du coût total d'une recette en se basant sur le salaire horaire moyen"), ("Suivi et alerte en temps réel et depuis votre mobile de la rentabilité d'une recette", "Suivi et alerte en temps réel et depuis votre mobile de la rentabilité d'une recette"), ("Aide au calcul du bon prix de vente d'une recette", "Aide au calcul du bon prix de vente d'une recette"), ('Aide à la créativité en proposant une interface indiquant les produits de saison', 'Aide à la créativité en proposant une interface indiquant les produits de saison'), ("Capacité à suivre l'évolution des prix d'un produit sur l'année", "Capacité à suivre l'évolution des prix d'un produit sur l'année"), ("Création d'une interface pour les clients permettant de consulter les allergènes et l'origine des produits d'une recette", "Création d'une interface pour les clients permettant de consulter les allergènes et l'origine des produits d'une recette"), ("Aide à la réalisation d'un inventaire", "Aide à la réalisation d'un inventaire"), ("Aide au respect des règles d'hygiène", "Aide au respect des règles d'hygiène"), ('Prémunission au turnover en sauvegardant vos recette, transmission du savoir', 'Prémunission au turnover en sauvegardant vos recette, transmission du savoir'), ('Gestion du linge', 'Gestion du linge')], max_length=125)),
                ('troisieme_fonctionnalite', models.CharField(blank=True, choices=[('Gestion des Commandes et Catalogues fournisseurs', 'Gestion des Commandes et Catalogues fournisseurs'), ('Gestion de la réception des Commandes et des Avoirs', 'Gestion de la réception des Commandes et des Avoirs'), ("Outil d'écriture et de stockage des recettes avec capacité de les partager aux membres de la cuisine ", "Outil d'écriture et de stockage des recettes avec capacité de les partager aux membres de la cuisine "), ('Scan intelligent des bons de réception/factures pour automatiser leur analyse ligne à ligne', 'Scan intelligent des bons de réception/factures pour automatiser leur analyse ligne à ligne'), ('Accès en temps réel à des données sur la masse et la répartition sur plusieurs critères des dépenses matière', 'Accès en temps réel à des données sur la masse et la répartition sur plusieurs critères des dépenses matière'), ('Calculateur intelligent de votre marge et de votre coefficient', 'Calculateur intelligent de votre marge et de votre coefficient'), ("Calculateur du coût total d'une recette en se basant sur le salaire horaire moyen", "Calculateur du coût total d'une recette en se basant sur le salaire horaire moyen"), ("Suivi et alerte en temps réel et depuis votre mobile de la rentabilité d'une recette", "Suivi et alerte en temps réel et depuis votre mobile de la rentabilité d'une recette"), ("Aide au calcul du bon prix de vente d'une recette", "Aide au calcul du bon prix de vente d'une recette"), ('Aide à la créativité en proposant une interface indiquant les produits de saison', 'Aide à la créativité en proposant une interface indiquant les produits de saison'), ("Capacité à suivre l'évolution des prix d'un produit sur l'année", "Capacité à suivre l'évolution des prix d'un produit sur l'année"), ("Création d'une interface pour les clients permettant de consulter les allergènes et l'origine des produits d'une recette", "Création d'une interface pour les clients permettant de consulter les allergènes et l'origine des produits d'une recette"), ("Aide à la réalisation d'un inventaire", "Aide à la réalisation d'un inventaire"), ("Aide au respect des règles d'hygiène", "Aide au respect des règles d'hygiène"), ('Prémunission au turnover en sauvegardant vos recette, transmission du savoir', 'Prémunission au turnover en sauvegardant vos recette, transmission du savoir'), ('Gestion du linge', 'Gestion du linge')], max_length=125)),
                ('player', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='form_and_game.player')),
            ],
        ),
        migrations.CreateModel(
            name='ExtraInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_title', models.CharField(max_length=150)),
                ('answer', models.TextField()),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='form_and_game.player')),
            ],
        ),
        migrations.CreateModel(
            name='ConnaissanceAchatFormAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('analyse_ligne_a_ligne_possible', models.CharField(choices=[('oui', 'oui'), ('non', 'non')], max_length=90)),
                ('gain_estime_si_ligne_a_ligne', models.IntegerField(validators=[django.core.validators.MinValueValidator(limit_value=0)])),
                ('methode_validation_paiement', models.CharField(choices=[('Votre signature sur la facture', 'je signe la facture'), ('Un tampon «Bon à payer»', "j'appose un tampon «Bon à payer» sur la facture"), ('Agrafage du bon de livraison avec la facture', "j'agrafe le bon de la livraison et la facture"), ('Remis en main propre à votre comptable', 'je les remets en main propre à mon comptable'), ('Autre', 'Autre')], max_length=90)),
                ('connaissance_moyenne_chiffree_des_achats', models.CharField(choices=[('Par semaine', 'par semaine'), ('Par décade', 'par décade'), ('Par mois', 'par mois'), ('Autre', 'autre'), ("Je n'y arrive pas", 'non, je ne la connais pas')], max_length=90)),
                ('connaissance_repartition_par_categorie', models.CharField(choices=[('oui', 'oui'), ('non', 'non')], max_length=90)),
                ('connaissance_quantite_par_fournisseur', models.CharField(choices=[('oui', 'oui'), ('non', 'non')], max_length=90)),
                ('unite_gain_ligne_a_ligne', models.CharField(choices=[('jour', 'jour'), ('semaine', 'semaine'), ('décade', 'décade'), ('mois', 'mois'), ('année', 'année')], max_length=90)),
                ('player', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='form_and_game.player')),
            ],
        ),
        migrations.CreateModel(
            name='ComptaFormAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('moyen_obtention_coefficients', models.CharField(choices=[('Moi même', 'par moi même'), ('Comptable', 'par mon comptable'), ('Autre', 'autre')], max_length=90)),
                ('support_comptablitie', models.CharField(max_length=90)),
                ('frequence_connaissance_coefficient', models.CharField(choices=[('Semaine', 'toutes les semaines'), ('Décade', 'toutes les décades'), ('Quinzaine', 'toutes les quinzaines'), ('Mensuelle', 'tous les mois'), ('Trimestrielle', 'tous les trimestres'), ('Semestrielle', 'tous les semestres'), ('Annuelle', 'tous les ans.')], max_length=90)),
                ('souhait_plus_de_regularite', models.CharField(choices=[('oui', 'oui'), ('non', 'non')], max_length=90)),
                ('depense_moyenne_obtention_bilan', models.IntegerField(validators=[django.core.validators.MinValueValidator(limit_value=0)])),
                ('unite_cout_optention_bilan', models.CharField(choices=[('mois', 'Mois'), ('an', 'An'), ('vacation', 'Vacation'), ('utilisation', 'Utilisation'), ('trimestre', 'Trimestre'), ('autre', 'Autre')], max_length=90)),
                ('depense_consentie_notre_version', models.IntegerField(validators=[django.core.validators.MinValueValidator(limit_value=0)])),
                ('player', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='form_and_game.player')),
            ],
        ),
        migrations.CreateModel(
            name='CommandeFormAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('methode_passage_commande', models.CharField(choices=[('Par téléphone en direct', 'par téléphone, en direct'), ('Par téléphone sur répondeur', 'par téléphone, sur répondeur'), ('Par mail', 'par mail'), ('Commercial', 'en communiquant avec un commercial'), ('Autre', 'Autre')], max_length=90)),
                ('frequence_passage_commande', models.CharField(choices=[('Tous les jours', 'tous les jours'), ('Tous les deux jours', 'tous les deux jours'), ('Une fois par semaine', 'une fois par semaine'), ('Autre', 'Autre')], max_length=90)),
                ('temps_passe_par_jour', models.IntegerField(validators=[django.core.validators.MinValueValidator(limit_value=0)])),
                ('temps_ideal_par_jour', models.IntegerField(validators=[django.core.validators.MinValueValidator(limit_value=0)])),
                ('support_memorisation', models.CharField(choices=[('Papier volant', 'sur papier volant'), ('Carnet', 'sur un carnet'), ('Informatiquement', 'sur un support informatique'), ('De tête', 'de tête'), ('Pas de mémorisation', '(et non, je ne les mémorise pas)'), ('Autre', 'Autre')], max_length=90)),
                ('methode_classement_commandes', models.CharField(choices=[("d'un classeur", "d'un classeur"), ("d'un trieur", "d'un trieur"), ("d'un ordinateur", "d'un ordinateur"), ('comptabilite', "d'envois à la comptabilité en direct"), ('non gardées', '(je ne les garde pas)'), ('Autre', 'Autre')], max_length=90)),
                ('methode_classement_bons_livraison', models.CharField(choices=[("d'un classeur", "d'un classeur"), ("d'un trieur", "d'un trieur"), ("d'un ordinateur", "d'un ordinateur"), ('comptabilite', "d'envois à la comptabilité en direct"), ('non gardées', '(je ne les garde pas)'), ('Autre', 'Autre')], max_length=90)),
                ('methode_classement_factures', models.CharField(choices=[("d'un classeur", "d'un classeur"), ("d'un trieur", "d'un trieur"), ("d'un ordinateur", "d'un ordinateur"), ('comptabilite', "d'envois à la comptabilité en direct"), ('Autre', 'Autre')], max_length=90)),
                ('methode_transmission_facture', models.CharField(choices=[('par mail', 'par mail'), ('par papier en direct', 'par papier, en direct'), ('en les scannant', 'en les scannant')], max_length=90)),
                ('proportion_factures_par_mail', models.CharField(choices=[('De 5% à 9%', 'De 5% à 9%'), ('De 10% à 29%', 'De 10% à 29%'), ('De 30% à 49%', 'De 30% à 49%'), ('De 50% à 79%', 'De 50% à 79%'), ('De 80% à 100%', 'De 80% à 100%')], max_length=90)),
                ('nombre_fournisseurs', models.IntegerField(validators=[django.core.validators.MinValueValidator(limit_value=0)])),
                ('player', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='form_and_game.player')),
            ],
        ),
        migrations.CreateModel(
            name='CarteFormAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frequence_modification', models.CharField(choices=[('Tous les jours', 'tous les jours'), ('Toutes les semaines', 'toutes les semaines'), ('Tous les mois', 'tous les mois'), ('Par saison', 'par saison'), ('Autre', 'autre')], max_length=90)),
                ('rythme_trouve_suffisant', models.CharField(choices=[('oui', 'oui'), ('non', 'non')], max_length=90)),
                ('frequence_suggestion_du_jour', models.CharField(choices=[("Je n'en fais pas", "je n'en fais pas"), ('Tous les jours', 'je les change tous les jours'), ('Tous les deux jours', 'je les change tous les deux jours'), ('Toutes les semaines', 'je les change toutes les semaines'), ('Autre', 'autre')], max_length=90)),
                ('methode_calcul_de_prix', models.CharField(choices=[('A la volée', 'à la volée'), ('Avec les prix les plus fort', 'avec les prix les plus fort'), ('Approximativement', 'approximativement'), ('Autre', 'Autre')], max_length=90)),
                ('prix_trouve_justes_clients', models.CharField(choices=[('Oui, suffisament juste', 'oui, suffisament justes'), ('Non', 'non'), ('Pas sûr', 'pas sûr')], max_length=90)),
                ('prix_trouve_justes_soi', models.CharField(choices=[('Oui, suffisament juste', 'oui, suffisament justes'), ('Non', 'non'), ('Pas sûr', 'pas sûr')], max_length=90)),
                ('player', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='form_and_game.player')),
            ],
        ),
        migrations.CreateModel(
            name='CallDemand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='form_and_game.player')),
            ],
        ),
    ]
