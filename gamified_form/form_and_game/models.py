from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.contrib.auth.models import PermissionsMixin
from .user_manager import UserManager
from django.utils import timezone
from form_and_game.badges import BADGES
from django.core.exceptions import ValidationError


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=20, blank=False)
    last_name = models.CharField(max_length=20, blank=False)
    email = models.EmailField(unique=True, blank=False)
    reset_password_token = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(
        ('active'),
        default=True,
        help_text=(
            'Designates whether this user should be '
            'treated as active. Unselect this instead '
            'of deleting accounts.'
        ),
    )
    is_superuser = models.BooleanField(
        ('staff status'),
        default=False,
        help_text=(
            'Designates whether the user can log into '
            'this admin site.'
        ),
    )
    is_staff = models.BooleanField(
        ('staff status'),
        default=False,
        help_text=(
            'Designates whether the user can log into '
            'this admin site.'
        ),
    )
    date_joined = models.DateTimeField(
        ('date joined'),
        default=timezone.now,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name}, {self.last_name}'
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        else:
            return ''

    def is_administrator(self):
        return self.is_superuser or self.is_staff

    def full_name_no_comma(self):
        return f"{self.first_name.lower()} {self.last_name.lower()}"


def player_directory_path(instance, filename):
    return 'pictures/{1}(id:{0})/{2}'.format(instance.user.id, instance.user.full_name(), filename)


class Player(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=16, validators=[
        RegexValidator(
            regex='/^(?:[0-8]\d|9[0-8])\d{3}$/',
            message='Phone number should be  8 or 13 digits long and can optionally be preceded by the country code followed by a space or a coma.',
            code='invalid_phone_number'
        )
    ])
    restaurant_name = models.CharField(max_length=100, blank=True)
    checking_picture = models.FileField(
        upload_to=player_directory_path, blank=True)
    to_contact_when_product_is_out = models.BooleanField(default=False)
    points = models.IntegerField(default=0, validators=[
                                 MinValueValidator(limit_value=0)])
    is_validated = models.BooleanField(default=False)

    def get_badge(self):
        max_score = 0
        user_badge = ""
        for badge in BADGES:
            if badge["max_points"] < self.points and badge["max_points"] > max_score:
                max_score = badge["max_points"]
                user_badge = badge
        return user_badge

    def get_badge_icon(self):
        return BADGES[self.get_badge()]["icon"]


class CarteFormAnswer(models.Model):
    class FrequenceModificationCarte(models.TextChoices):
        TOUTES_SEMAINES = 'Toutes les semaines'
        TOUS_MOIS = 'Tous les mois'
        PAR_SAISON = 'Par saison'
        AUTRES = 'Autre'

    class FrequenceSuggestionJour(models.TextChoices):
        JAMAIS = "Je n'en ai fait pas"
        TOUS_JOURS = 'Tous les jours'
        TOUS_DEUX_JOURS = 'Tous les deux jours'
        TOUTES_SEMAINES = 'Toutes les semaines'
        AUTRE = 'Autre'

    class MethodesCalculPrix(models.TextChoices):
        VOLEE = "A la volée"
        PRIX_FORTS = "Avec les prix les plus fort"
        APPROXIMATIVEMENT = "Approximativement"
        AUTRE = "Autre"
        # AUTRES TYPE?

    class MesuresJustessePrix(models.TextChoices):
        OUI = "Oui, suffisament juste"
        NON = "Non"
        PAS_SUR = "Pas sûr"

    player = models.OneToOneField(
        Player, on_delete=models.SET_NULL, null=True)
    frequence_modification = models.CharField(
        choices=FrequenceModificationCarte.choices, blank=False, max_length=90)
    rythme_trouve_suffisant = models.BooleanField(default=False)
    frequence_suggestion_du_jour = models.CharField(
        choices=FrequenceSuggestionJour.choices, blank=False, max_length=90)
    methode_calcul_de_prix = models.CharField(
        choices=MethodesCalculPrix.choices, blank=False, max_length=90)
    prix_trouve_justes = models.CharField(
        choices=MesuresJustessePrix.choices, blank=False, max_length=90)
    gain_estime_si_plus_precis = models.IntegerField(
        default=0, validators=[MinValueValidator(limit_value=0)])


class RecetteFormAnswer(models.Model):
    class SupportsMemorisation(models.TextChoices):
        PAPIER_VOLANT = "Sur du papier volant"
        CARNET = "Sur un carnet"
        EXCEL = "Excel ou autre tableur"
        WORD = "Word ou autre éditeur"
        INFORMATIQUEMENT = "Autre outil informatique"
        AUTRE = "Autre"

    class MethodesTransmissionSavoir(models.TextChoices):
        ORALEMENT = "Oralement"
        PAPIER_VOLANT = "Sur papier volant"
        CLASSEUR = "Dans un classeur"
        AUTRE = "Autre"

    player = models.OneToOneField(
        Player, on_delete=models.SET_NULL, null=True)
    support_memorisation = models.CharField(
        choices=SupportsMemorisation.choices, blank=False, max_length=90)
    satisfait_support_memorisation = models.BooleanField(default=False)
    temps_passe_par_mois = models.IntegerField(default=0,
                                               validators=[MinValueValidator(limit_value=0)])
    est_ce_trop = models.BooleanField(blank=False)
    methode_transmission_savoir = models.CharField(
        choices=MethodesTransmissionSavoir.choices, blank=False, max_length=90)
    satisfait_mode_transmission = models.BooleanField(default=False)
    # COMMENT ON MESURE LE TURNOVER?


class CommandeFormAnswer(models.Model):
    class MethodesPassageCommande(models.TextChoices):
        TELEPHONE_DIRECT = "Par téléphone en direct"
        TELEPHONE_REPONDEUR = "Par téléphone sur répondeur"
        MAIL = "Par mail"
        COMMERCIAL = "Commercial"
        AUTRE = "Autre"

    class FrequencesPassageCommande(models.TextChoices):
        TOUS_JOURS = "Tous les jours"
        TOUS_DEUX_JOURS = "Tous les deux jours"
        TOUTES_SEMAINES = "Une fois par semaine"
        AUTRE = "Autre"

    class SupportsMemorisation(models.TextChoices):
        PAPIER_VOLANT = "Papier volant"
        CARNET = "Carnet"
        INFORMATIQUEMENT = "Informatiquement"
        DE_TETE = "De tête"
        NONE = "Pas de mémorisation"
        AUTRE = "Autre"

    class MethodesClassement(models.TextChoices):
        AUTRE = "Autre"
        # WHICH??

    class MethodesTransmissionFactures(models.TextChoices):
        MAIL = "par mail"
        PAPIER = "par papier en direct"
        SCAN = "en les scannant"

    class ProportionsFacturesParMail(models.TextChoices):
        DE_5_A_9 = "De 5% à 9%"
        DE_10_A_29 = "De 10% à 29%"
        DE_30_A_49 = "De 30% à 49%"
        DE_50_A_79 = "De 50% à 79%"
        DE_80_A_100 = "De 80% à 100%"

    player = models.OneToOneField(
        Player, on_delete=models.SET_NULL, null=True)
    methode_passage_commande = models.CharField(
        choices=MethodesPassageCommande.choices, blank=False, max_length=90)
    frequence_passage_commande = models.CharField(
        choices=FrequencesPassageCommande.choices, blank=False, max_length=90)
    temps_passe_par_jour = models.IntegerField(
        validators=[MinValueValidator(limit_value=0)], blank=False)
    temps_ideal_par_jour = models.IntegerField(
        validators=[MinValueValidator(limit_value=0)], blank=False)
    support_memorisation = models.CharField(
        choices=SupportsMemorisation.choices, blank=False, max_length=90)
    methode_classement_commandes = models.CharField(
        choices=MethodesClassement.choices, blank=False, max_length=90)
    methode_classement_bons_livraison = models.CharField(
        choices=MethodesClassement.choices, blank=False, max_length=90)
    methode_classement_factures = models.CharField(
        choices=MethodesClassement.choices, blank=False, max_length=90)
    methode_transmission_facture = models.CharField(
        choices=MethodesTransmissionFactures.choices, blank=False, max_length=90)
    proportion_factures_par_mail = models.CharField(
        choices=ProportionsFacturesParMail.choices, blank=False, max_length=90)


class ConnaissanceAchatFormAnswer(models.Model):
    class MethodesVerificationPaiement(models.TextChoices):
        SIGNATURE = "Votre signature sur la facture"
        TAMPON = "Un tampon «Bon à payer»"
        AGRAFAGE = "Agrafage du bon de livraison avec la facture"
        REMIS = "Remis en main propre à votre comptable"
        AUTRE = "Autre"

    class PeriodesConnaissanceMoyenneAchats(models.TextChoices):
        SEMAINE = "Par semaine"
        DECADE = "Par décade"
        MOIS = "Par mois"
        AUTRE = "Autre"

    player = models.OneToOneField(
        Player, on_delete=models.SET_NULL, null=True)
    analyse_ligne_a_ligne_possible = models.BooleanField(default=False)
    gain_estime_si_ligne_a_ligne = models.IntegerField(
        default=0, validators=[MinValueValidator(limit_value=0)])
    methode_validation_paiement = models.CharField(
        choices=MethodesVerificationPaiement.choices, blank=False, max_length=90)
    connaissance_moyenne_chiffree_des_achats = models.CharField(
        choices=PeriodesConnaissanceMoyenneAchats.choices, blank=False, max_length=90)
    connaissance_moyenne_des_achats = models.BooleanField(default=False)
    connaissance_repartition_par_categorie = models.BooleanField(default=True)
    connaissance_quantite_par_fournisseur = models.BooleanField(default=True)
    connaissance_cout = models.BooleanField(default=True)


class ComptaFormAnswer(models.Model):
    class FrequencesConnaissanceCoefficients(models.TextChoices):
        SEMAINE = "Semaine"
        DECADE = "Décade"
        QUINZAINE = "Quinzaine"
        MENSUELLE = "Mensuelle"
        TRIMESTRIELLE = "Trimestrielle"
        SEMESTRIELLE = "Semestrielle"
        ANNUELLE = "Annuelle"

    player = models.OneToOneField(
        Player, on_delete=models.SET_NULL, null=True)
    moyen_obtention_coefficients = models.CharField(max_length=90, blank=False)
    support_comptablitie = models.CharField(max_length=90, blank=False)
    outil_utilise = models.CharField(max_length=60, blank=True)
    frequence_connaissance_coefficient = models.CharField(
        choices=FrequencesConnaissanceCoefficients.choices, blank=False, max_length=90)
    souhait_plus_de_regularite = models.BooleanField(blank=False)
    depense_moyenne_obtention_bilan = models.IntegerField(
        validators=[MinValueValidator(limit_value=0)], blank=False)
    depense_consentie_notre_version = models.IntegerField(
        validators=[MinValueValidator(limit_value=0)], blank=False)


class FonctionnalitesPrefereesFormAnswer(models.Model):
    class Fonctionnalites(models.TextChoices):
        SEMAINE = "Semaine"
        DECADE = "Décade"
        QUINZAINE = "Quinzaine"
        MENSUELLE = "Mensuelle"
        TRIMESTRIELLE = "Trimestrielle"
        SEMESTRIELLE = "Semestrielle"
        ANNUELLE = "Annuelle"

    player = models.OneToOneField(
        Player, on_delete=models.SET_NULL, null=True)
    premiere_fonctionnalite = models.CharField(
        choices=Fonctionnalites.choices, blank=False, max_length=90)
    deuxieme_fonctionnalite = models.CharField(
        choices=Fonctionnalites.choices, blank=False, max_length=90)
    troisieme_fonctionnalite = models.CharField(
        choices=Fonctionnalites.choices, blank=False, max_length=90)

    def clean(self):
        if self.premiere_fonctionnalite == self.deuxieme_fonctionnalite or self.deuxieme_fonctionnalite == self.troisieme_fonctionnalite or self.troisieme_fonctionnalite == self.premiere_fonctionnalite:
            raise ValidationError(
                "Choisis trois fonctionnalités différentes, s'il te plaît!")


class GeneralIntroductionFormAnswer(models.Model):
    class Metiers(models.TextChoices):
        CHEF_PROPRIETAIRE = "Chef de cuisine et pâtissier propriétaire", (
            "Chef de cuisine et pâtissier propriétaire")
        CHEF_SALARIE_ACTIONNAIRE = "Chef de cuisine et pâtissier salarié actionnaire", (
            "Chef de cuisine et pâtissier salarié actionnaire")
        CHEF_SALARIE = "Chef de cuisine et pâtissier salarié", (
            "Chef de cuisine et pâtissier salarié")

    player = models.OneToOneField(
        Player, on_delete=models.SET_NULL, null=True)
    metier = models.CharField(
        choices=Metiers.choices, blank=False, max_length=90)
    ville = models.CharField(max_length=35, blank=False)
    age = models.IntegerField(
        validators=[MinValueValidator(limit_value=0)], blank=False)
    experience = models.IntegerField(
        validators=[MinValueValidator(limit_value=0)], blank=False)
    nombre_couverts = models.IntegerField(
        validators=[MinValueValidator(limit_value=0)], blank=False)
    nombre_places = models.IntegerField(
        validators=[MinValueValidator(limit_value=0)], blank=False)
    nombre_cuisiniers = models.IntegerField(
        validators=[MinValueValidator(limit_value=0)], blank=False)
    prix_moyen_assiette = models.DecimalField(decimal_places=2,
                                              validators=[MinValueValidator(limit_value=0)], blank=False, max_digits=5)
    nombre_etablissements = models.IntegerField(
        default=1, validators=[MinValueValidator(limit_value=1)])
