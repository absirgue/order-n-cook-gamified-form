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
    accepted_conditions = models.BooleanField(default=False)
    sharing_code = models.CharField(max_length=20, blank=False)
    randomly_created = models.BooleanField(default=False)
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
        full_name = f"{self.first_name.lower()} {self.last_name.lower()}"
        return ' '.join(elem.capitalize() for elem in full_name.split())

    def get_group(self):
        if self.is_administrator():
            return "Administrator"
        else:
            return "Player"


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
    needs_precising = models.BooleanField(default=True)
    was_added_precision_points = models.BooleanField(default=False)
    booked_phone_call = models.BooleanField(default=False)

    def get_status(self):
        min_score = 100000
        user_badge = ""
        for badge in BADGES:
            if BADGES[badge]["max_points"] > self.points and BADGES[badge]["max_points"] < min_score:
                min_score = BADGES[badge]["max_points"]
                user_badge = BADGES[badge]
        return user_badge

    def get_badge(self):
        return self.get_status()['icon']
    
    def get_status_name(self):
        status_name = self.get_status()['title']
        return ' '.join(elem.capitalize() for elem in status_name.split())

    def get_progress_percentage(self):
        return self.points*100/self.get_status()["max_points"]

class SharingAlert(models.Model):
    user = models.ForeignKey(
        User,on_delete=models.SET_NULL,null=True)
    text = models.CharField(max_length=100,blank=False)
    was_shared = models.BooleanField(default=False)

class CarteFormAnswer(models.Model):
    class FrequenceModificationCarte(models.TextChoices):
        TOUS_JOURS = 'Tous les jours', ('tous les jours')
        TOUTES_SEMAINES = 'Toutes les semaines', ('toutes les semaines')
        TOUS_MOIS = 'Tous les mois', ('tous les mois')
        PAR_SAISON = 'Par saison', ('par saison')
        AUTRES = 'Autre',("autre")

    class FrequenceSuggestionJour(models.TextChoices):
        JAMAIS = "Je n'en fais pas", ("je n'en fais pas")
        TOUS_JOURS = 'Tous les jours', ("je les change tous les jours")
        TOUS_DEUX_JOURS = 'Tous les deux jours', (
            "je les change tous les deux jours")
        TOUTES_SEMAINES = 'Toutes les semaines', (
            "je les change toutes les semaines")
        AUTRE = 'Autre',("autre")

    class MethodesCalculPrix(models.TextChoices):
        VOLEE = "A la volée", ('à la volée')
        PRIX_FORTS = "Avec les prix les plus fort", (
            "avec les prix les plus fort")
        APPROXIMATIVEMENT = "Approximativement", ("approximativement")
        AUTRE = "Autre"
        # AUTRES TYPE?

    class MesuresJustessePrix(models.TextChoices):
        OUI = "Oui, suffisament juste", ("oui, suffisament justes")
        NON = "Non",("non")
        PAS_SUR = "Pas sûr", ("pas sûr")
    
    class OUIouNON(models.TextChoices):
        OUI = "oui",("oui")
        NON = "non",("non")


    player = models.OneToOneField(
        Player, on_delete=models.SET_NULL, null=True)
    frequence_modification = models.CharField(
        choices=FrequenceModificationCarte.choices, blank=False, max_length=90)
    rythme_trouve_suffisant = models.CharField(
        choices=OUIouNON.choices, blank=False, max_length=90)
    frequence_suggestion_du_jour = models.CharField(
        choices=FrequenceSuggestionJour.choices, blank=False, max_length=90)
    methode_calcul_de_prix = models.CharField(
        choices=MethodesCalculPrix.choices, blank=False, max_length=90)
    prix_trouve_justes_clients = models.CharField(
        choices=MesuresJustessePrix.choices, blank=False, max_length=90)
    prix_trouve_justes_soi = models.CharField(
        choices=MesuresJustessePrix.choices, blank=False, max_length=90)


class RecetteFormAnswer(models.Model):
    class SupportsMemorisation(models.TextChoices):
        PAPIER_VOLANT = "sur du papier volant", ("sur du papier volant")
        CARNET = "Sur un carnet", ("sur un carnet")
        EXCEL = "Excel ou autre tableur", ("sur Excel ou un autre tableur")
        WORD = "Word ou autre éditeur", ("sur Word ou autre éditeur")
        INFORMATIQUEMENT = "Autre outil informatique", (
            "grâce à un autre outil informatique")
        AUTRE = "Autre",("autre")

    class MethodesTransmissionSavoir(models.TextChoices):
        ORALEMENT = "Oralement", ("oralement")
        PAPIER_VOLANT = "Sur papier volant", ("sur papier volant")
        CLASSEUR = "Dans un classeur", ("à l'aide de classeurs")
        AUTRE = "Autre",("autre")
    
    class OUIouNON(models.TextChoices):
        OUI = "oui",("oui")
        NON = "non",("non")


    player = models.OneToOneField(
        Player, on_delete=models.SET_NULL, null=True)
    support_memorisation = models.CharField(
        choices=SupportsMemorisation.choices, blank=False, max_length=90)
    satisfait_support_memorisation =models.CharField(
        choices=OUIouNON.choices, blank=False, max_length=90)
    temps_passe_minute_par_recette = models.IntegerField(
        validators=[MinValueValidator(limit_value=0)], blank=False)
    est_ce_trop = models.CharField(
        choices=OUIouNON.choices, blank=False, max_length=90)
    methode_transmission_savoir = models.CharField(
        choices=MethodesTransmissionSavoir.choices, blank=False, max_length=90)
    satisfait_mode_transmission = models.CharField(
        choices=OUIouNON.choices, blank=False, max_length=90)
    # COMMENT ON MESURE LE TURNOVER?


class CommandeFormAnswer(models.Model):
    class MethodesPassageCommande(models.TextChoices):
        TELEPHONE_DIRECT = "Par téléphone en direct", (
            "par téléphone, en direct")
        TELEPHONE_REPONDEUR = "Par téléphone sur répondeur", (
            "par téléphone, sur répondeur")
        MAIL = "Par mail", ("par mail")
        COMMERCIAL = "Commercial", ("en communiquant avec un commercial")
        AUTRE = "Autre"

    class FrequencesPassageCommande(models.TextChoices):
        TOUS_JOURS = "Tous les jours", ("tous les jours")
        TOUS_DEUX_JOURS = "Tous les deux jours", ("tous les deux jours")
        TOUTES_SEMAINES = "Une fois par semaine", ("une fois par semaine")
        AUTRE = "Autre"

    class SupportsMemorisation(models.TextChoices):
        PAPIER_VOLANT = "Papier volant", ("sur papier volant")
        CARNET = "Carnet", ("sur un carnet")
        INFORMATIQUEMENT = "Informatiquement", ("sur un support informatique")
        DE_TETE = "De tête", ("de tête")
        NONE = "Pas de mémorisation", ("(et non, je ne les mémorise pas)")
        AUTRE = "Autre"

    class MethodesClassementAutres(models.TextChoices):
        CLASSEUR = "classeur"
        TRIEUR = "trieur"
        ORDINATEUR = "ordinateur"
        COMPTABILITE = "comptabilite", ("envoi à la comptabilité en direct")
        NON_CONSERVEES = "non gardées", ("(je ne les garde pas)")
        AUTRE = "Autre"
    
    class MethodesClassementFactures(models.TextChoices):
        CLASSEUR = "classeur"
        TRIEUR = "trieur"
        ORDINATEUR = "ordinateur"
        COMPTABILITE = "comptabilite", ("envoi à la comptabilité en direct")
        AUTRE = "Autre"

    class MethodesTransmissionFactures(models.TextChoices):
        MAIL = "par mail", ("par mail")
        PAPIER = "par papier en direct", ("par papier, en direct")
        SCAN = "en les scannant", ("en les scannant")

    class ProportionsFacturesParMail(models.TextChoices):
        DE_5_A_9 = "De 5% à 9%", ("De 5% à 9%")
        DE_10_A_29 = "De 10% à 29%", ("De 10% à 29%")
        DE_30_A_49 = "De 30% à 49%", ("De 30% à 49%")
        DE_50_A_79 = "De 50% à 79%", ("De 50% à 79%")
        DE_80_A_100 = "De 80% à 100%", ("De 80% à 100%")

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
        choices=MethodesClassementAutres.choices, blank=False, max_length=90)
    methode_classement_bons_livraison = models.CharField(
        choices=MethodesClassementAutres.choices, blank=False, max_length=90)
    methode_classement_factures = models.CharField(
        choices=MethodesClassementFactures.choices, blank=False, max_length=90)
    methode_transmission_facture = models.CharField(
        choices=MethodesTransmissionFactures.choices, blank=False, max_length=90)
    proportion_factures_par_mail = models.CharField(
        choices=ProportionsFacturesParMail.choices, blank=False, max_length=90)
    nombre_fournisseurs = models.IntegerField(
        validators=[MinValueValidator(limit_value=0)], blank=False)


class ConnaissanceAchatFormAnswer(models.Model):
    class MethodesVerificationPaiement(models.TextChoices):
        SIGNATURE = "Votre signature sur la facture", ("je signe la facture")
        TAMPON = "Un tampon «Bon à payer»", (
            "j'appose un tampon «Bon à payer» sur la facture")
        AGRAFAGE = "Agrafage du bon de livraison avec la facture", (
            "j'agrafe le bon de la livraison et la facture")
        REMIS = "Remis en main propre à votre comptable", (
            "je les remets en main propre à mon comptable")
        AUTRE = "Autre"

    class PeriodesConnaissanceMoyenneAchats(models.TextChoices):
        SEMAINE = "Par semaine",("par semaine")
        DECADE = "Par décade",("par décade")
        MOIS = "Par mois",("par mois")
        AUTRE = "Autre",("autre")
    
    class UnitesGainLigneALigne(models.TextChoices):
        JOUR = "jour",("jour")
        SEMAINE = "semaine",("semaine")
        DECADE = "décade",("décade")
        MOIS = "mois",("mois")
        ANNEE = "année",("année")

    class OUIouNON(models.TextChoices):
        OUI = "oui",("oui")
        NON = "non",("non")

    player = models.OneToOneField(
        Player, on_delete=models.SET_NULL, null=True)
    analyse_ligne_a_ligne_possible = models.CharField(
        choices=OUIouNON.choices, blank=False, max_length=90)
    gain_estime_si_ligne_a_ligne = models.IntegerField(validators=[MinValueValidator(limit_value=0)])
    methode_validation_paiement = models.CharField(
        choices=MethodesVerificationPaiement.choices, blank=False, max_length=90)
    connaissance_moyenne_chiffree_des_achats = models.CharField(
        choices=PeriodesConnaissanceMoyenneAchats.choices, blank=False, max_length=90)
    connaissance_repartition_par_categorie =  models.CharField(
        choices=OUIouNON.choices, blank=False, max_length=90)
    connaissance_quantite_par_fournisseur =  models.CharField(
        choices=OUIouNON.choices, blank=False, max_length=90)
    unite_gain_ligne_a_ligne = models.CharField(
        choices=UnitesGainLigneALigne.choices, blank=False, max_length=90)


class ComptaFormAnswer(models.Model):

    class MoyensObtentionCoefficients(models.TextChoices):
        MOI_MEME = "Moi même", ("par moi même")
        PAR_MON_COMPTABLE = "Comptable", ("par mon comptable")
        AUTRE = "Autre", ("autre")

    class SupportsCompta(models.TextChoices):
        TABLEUR = "Papier", ("papier")
        PAPIER = "un Tableur", ("un tableur")
        AUTRE = "Autre", ("autre")

    class FrequencesConnaissanceCoefficients(models.TextChoices):
        SEMAINE = "Semaine", ("toutes les semaines")
        DECADE = "Décade", ("toutes les décades")
        QUINZAINE = "Quinzaine", ("toutes les quinzaines")
        MENSUELLE = "Mensuelle", ("tous les mois")
        TRIMESTRIELLE = "Trimestrielle", ("tous les trimestres")
        SEMESTRIELLE = "Semestrielle", ("tous les semestres")
        ANNUELLE = "Annuelle", ("tous les ans.")

    class OUIouNON(models.TextChoices):
        OUI = "oui",("oui")
        NON = "non",("non")

    class UnitesCoutSystemeActuel(models.TextChoices):
        MOIS = "mois"
        AN = "an"
        VACATION = "vacation"
        UTILISATION = "utilisation"
        TRIMESTRE = "trimestre"
        AUTRE = "autre"

    player = models.OneToOneField(
        Player, on_delete=models.SET_NULL, null=True)
    moyen_obtention_coefficients = models.CharField(
        choices=MoyensObtentionCoefficients.choices, blank=False, max_length=90)
    support_comptablitie = models.CharField(max_length=90, blank=False)
    outil_utilise = models.CharField(max_length=60, blank=True)
    frequence_connaissance_coefficient = models.CharField(
        choices=FrequencesConnaissanceCoefficients.choices, blank=False, max_length=90)
    souhait_plus_de_regularite = models.CharField(
        choices=OUIouNON.choices, blank=False, max_length=90)
    depense_moyenne_obtention_bilan = models.IntegerField(
        validators=[MinValueValidator(limit_value=0)], blank=False)
    unite_cout_optention_bilan = models.CharField(
        choices=UnitesCoutSystemeActuel.choices, blank=False, max_length=90)
    depense_consentie_notre_version = models.IntegerField(
        validators=[MinValueValidator(limit_value=0)], blank=False)


class FonctionnalitesPrefereesFormAnswer(models.Model):
    class Fonctionnalites(models.TextChoices):
        COMMANDES_FOURNISSEURS = "Gestion des Commandes et Catalogues fournisseurs",("Gestion des Commandes et Catalogues fournisseurs")
        RECEPTION_AVOIRS = "Gestion de la réception des Commandes et des Avoirs",("Gestion de la réception des Commandes et des Avoirs")
        RECETTES = "Outil d'écriture et de stockage des recettes avec capacité de les partager aux membres de la cuisine ", ("Outil d'écriture et de stockage des recettes avec capacité de les partager aux membres de la cuisine ")
        SCAN = "Scan intelligent des bons de réception/factures pour automatiser leur analyse ligne à ligne", ("Scan intelligent des bons de réception/factures pour automatiser leur analyse ligne à ligne")
        DONNEES_TEMPS_REEL = "Accès en temps réel à des données sur la masse et la répartition sur plusieurs critères des dépenses matière",("Accès en temps réel à des données sur la masse et la répartition sur plusieurs critères des dépenses matière")
        CALCUL_MARGE_COEFF = "Calculateur intelligent de votre marge et de votre coefficient",("Calculateur intelligent de votre marge et de votre coefficient")
        CALCUL_COUT_TOTAL = "Calculateur du coût total d'une recette en se basant sur le salaire horaire moyen",("Calculateur du coût total d'une recette en se basant sur le salaire horaire moyen")
        SUIVI_ALERTES = "Suivi et alerte en temps réel et depuis votre mobile de la rentabilité d'une recette", ("Suivi et alerte en temps réel et depuis votre mobile de la rentabilité d'une recette")
        CALCUL_PRIX_VENTE ="Aide au calcul du bon prix de vente d'une recette",("Aide au calcul du bon prix de vente d'une recette")
        AIDE_CREATIVITE = "Aide à la créativité en proposant une interface indiquant les produits de saison",("Aide à la créativité en proposant une interface indiquant les produits de saison")
        EVOLUTION_PRIX = "Capacité à suivre l'évolution des prix d'un produit sur l'année", ("Capacité à suivre l'évolution des prix d'un produit sur l'année")
        INTERFACE_CLIENT = "Création d'une interface pour les clients permettant de consulter les allergènes et l'origine des produits d'une recette",("Création d'une interface pour les clients permettant de consulter les allergènes et l'origine des produits d'une recette")
        INVENTAIRE = "Aide à la réalisation d'un inventaire",("Aide à la réalisation d'un inventaire")
        HYGIENE = "Aide au respect des règles d'hygiène",("Aide au respect des règles d'hygiène")
        TURNOVER = "Prémunission au turnover en sauvegardant vos recette, transmission du savoir",("Prémunission au turnover en sauvegardant vos recette, transmission du savoir")
        GESTION_LINGE = "Gestion du linge",("Gestion du linge")


    player = models.OneToOneField(
        Player, on_delete=models.SET_NULL, null=True)
    premiere_fonctionnalite = models.CharField(
        choices=Fonctionnalites.choices, blank=False, max_length=125)
    deuxieme_fonctionnalite = models.CharField(
        choices=Fonctionnalites.choices, blank=False, max_length=125)
    troisieme_fonctionnalite = models.CharField(
        choices=Fonctionnalites.choices, blank=True, max_length=125)

    def clean(self):
        if self.premiere_fonctionnalite == self.deuxieme_fonctionnalite or self.deuxieme_fonctionnalite == self.troisieme_fonctionnalite or self.troisieme_fonctionnalite == self.premiere_fonctionnalite:
            raise ValidationError(
                "Choisis trois fonctionnalités différentes, s'il te plaît!")


class GeneralIntroductionFormAnswer(models.Model):
    class Metiers(models.TextChoices):
        CHEF_PROPRIETAIRE = "Chef de cuisine et pâtissier propriétaire", (
            "chef de cuisine et pâtissier propriétaire")
        CHEF_SALARIE_ACTIONNAIRE = "Chef de cuisine et pâtissier salarié actionnaire", (
            "chef de cuisine et pâtissier salarié actionnaire")
        CHEF_SALARIE = "Chef de cuisine et pâtissier salarié", (
            "chef de cuisine et pâtissier salarié")

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

class ExtraInformation(models.Model):
    player = models.ForeignKey(
        Player, on_delete=models.SET_NULL, null=True)
    field_title = models.CharField(max_length=150)
    answer = models.TextField()

class CallDemand(models.Model):
    player = models.ForeignKey(
        Player, on_delete=models.SET_NULL, null=True)