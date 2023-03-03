from django import forms
from form_and_game.models import *

class FonctionnalitesPrefereesForm(forms.ModelForm):
    class Meta:
        model = FonctionnalitesPrefereesFormAnswer
        fields = ['premiere_fonctionnalite', 'deuxieme_fonctionnalite', 'troisieme_fonctionnalite']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update(
                {'class': 'default-input'})

    def save(self, _user):
        """Create a new user"""
        super().save(commit=False)
        answer = FonctionnalitesPrefereesFormAnswer.objects.create(
            player=Player.objects.get(user=_user),
            premiere_fonctionnalite=self.cleaned_data.get(
                'premiere_fonctionnalite'),
            deuxieme_fonctionnalite=self.cleaned_data.get(
                'deuxieme_fonctionnalite'),
            troisieme_fonctionnalite=self.cleaned_data.get(
                'troisieme_fonctionnalite')
        )
        return answer

class PasswordEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['password']

class ComptaForm(forms.ModelForm):
    class Meta:
        model = ComptaFormAnswer
        fields = ['moyen_obtention_coefficients', 'support_comptablitie',
                  'frequence_connaissance_coefficient', 'souhait_plus_de_regularite', 'depense_moyenne_obtention_bilan', 'depense_consentie_notre_version']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update(
                {'class': 'default-input'})
        self.fields['support_comptablitie'].widget.attrs.update(
            {'placeholder': "nom de l'outil"})

    def save(self, _user):
        """Create a new user"""
        super().save(commit=False)
        answer = ComptaFormAnswer.objects.create(
            player=Player.objects.get(user=_user),
            moyen_obtention_coefficients=self.cleaned_data.get(
                'moyen_obtention_coefficients'),
            support_comptablitie=self.cleaned_data.get(
                'support_comptablitie'),
            frequence_connaissance_coefficient=self.cleaned_data.get(
                'frequence_connaissance_coefficient'),
            souhait_plus_de_regularite=self.cleaned_data.get(
                'souhait_plus_de_regularite'),
            depense_moyenne_obtention_bilan=self.cleaned_data.get(
                'depense_moyenne_obtention_bilan'),
            depense_consentie_notre_version=self.cleaned_data.get(
                'depense_consentie_notre_version'),
        )
        return answer


class ConnaissanceAchatForm(forms.ModelForm):
    class Meta:
        model = ConnaissanceAchatFormAnswer
        fields = ['analyse_ligne_a_ligne_possible', 'gain_estime_si_ligne_a_ligne', 'methode_validation_paiement',
                  'connaissance_moyenne_chiffree_des_achats', 'connaissance_repartition_par_categorie', 'connaissance_quantite_par_fournisseur','unite_gain_ligne_a_ligne']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update(
                {'class': 'default-input'})

    def save(self, _user):
        """Create a new user"""
        super().save(commit=False)
        answer = ConnaissanceAchatFormAnswer.objects.create(
            player=Player.objects.get(user=_user),
            analyse_ligne_a_ligne_possible=self.cleaned_data.get(
                'analyse_ligne_a_ligne_possible'),
            gain_estime_si_ligne_a_ligne=self.cleaned_data.get(
                'gain_estime_si_ligne_a_ligne'),
            methode_validation_paiement=self.cleaned_data.get(
                'methode_validation_paiement'),
            connaissance_moyenne_chiffree_des_achats=self.cleaned_data.get(
                'connaissance_moyenne_chiffree_des_achats'),
            connaissance_repartition_par_categorie=self.cleaned_data.get(
                'connaissance_repartition_par_categorie'),
            connaissance_quantite_par_fournisseur=self.cleaned_data.get(
                'connaissance_quantite_par_fournisseur'),
            unite_gain_ligne_a_ligne = self.cleaned_data.get(
                'unite_gain_ligne_a_ligne'),
        )
        return answer


class CommandeForm(forms.ModelForm):
    class Meta:
        """Form options."""
        model = CommandeFormAnswer
        fields = ['methode_passage_commande', 'frequence_passage_commande', 'temps_passe_par_jour', 'temps_ideal_par_jour',
                  'support_memorisation', 'methode_classement_commandes', 'methode_classement_bons_livraison', 'methode_classement_factures', 'methode_transmission_facture', 'proportion_factures_par_mail','nombre_fournisseurs']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update(
                {'class': 'default-input'})

    def save(self, _user):
        """Create a new user"""
        super().save(commit=False)
        answer = CommandeFormAnswer.objects.create(
            player=Player.objects.get(user=_user),
            methode_passage_commande=self.cleaned_data.get(
                'methode_passage_commande'),
            frequence_passage_commande=self.cleaned_data.get(
                'frequence_passage_commande'),
            temps_passe_par_jour=self.cleaned_data.get('temps_passe_par_jour'),
            temps_ideal_par_jour=self.cleaned_data.get('temps_ideal_par_jour'),
            support_memorisation=self.cleaned_data.get(
                'support_memorisation'),
            methode_classement_commandes=self.cleaned_data.get(
                'methode_classement_commandes'),
            methode_classement_bons_livraison=self.cleaned_data.get(
                'methode_classement_bons_livraison'),
            methode_classement_factures=self.cleaned_data.get(
                'methode_classement_factures'),
            methode_transmission_facture=self.cleaned_data.get(
                'methode_transmission_facture'),
            proportion_factures_par_mail=self.cleaned_data.get(
                'proportion_factures_par_mail'),
            nombre_fournisseurs =self.cleaned_data.get(
                'nombre_fournisseurs'),
        )
        return answer


class RecetteForm(forms.ModelForm):
    class Meta:
        """Form options."""
        model = RecetteFormAnswer
        fields = ['support_memorisation', 'satisfait_support_memorisation', 'temps_passe_minute_par_recette', 'est_ce_trop',
                  'methode_transmission_savoir', 'satisfait_mode_transmission']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update(
                {'class': 'default-input'})

    def save(self, _user):
        """Create a new user"""
        super().save(commit=False)
        answer = RecetteFormAnswer.objects.create(
            player=Player.objects.get(user=_user),
            support_memorisation=self.cleaned_data.get('support_memorisation'),
            satisfait_support_memorisation=self.cleaned_data.get(
                'satisfait_support_memorisation'),
            temps_passe_minute_par_recette=self.cleaned_data.get('temps_passe_minute_par_recette'),
            est_ce_trop=self.cleaned_data.get('est_ce_trop'),
            methode_transmission_savoir=self.cleaned_data.get(
                'methode_transmission_savoir'),
            satisfait_mode_transmission=self.cleaned_data.get(
                'satisfait_mode_transmission'),
        )
        return answer

class LogInForm(forms.Form):
    """Form enabling registered users to log in."""
    email = forms.CharField(label="Email")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update(
                {'class': 'default-input log_in_fields'})
        self.fields['email'].widget.attrs.update(
            {'placeholder': 'E-mail'})
        self.fields['password'].widget.attrs.update(
            {'placeholder': 'Mot de passe'})

class GeneralInformationForm(forms.ModelForm):
    class Meta:
        """Form options."""
        model = GeneralIntroductionFormAnswer
        fields = ['metier', 'ville', 'age', 'nombre_couverts',
                  'nombre_cuisiniers', 'prix_moyen_couvert', 'nombre_etablissements', 'experience', 'nombre_places']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update(
                {'class': 'default-input'})
        self.fields['ville'].widget.attrs.update(
            {'placeholder': 'ville'})
        self.fields['age'].widget.attrs.update(
            {'placeholder': 'âge'})
        self.fields['experience'].widget.attrs.update(
            {'placeholder': "nombre d'années"})
        self.fields['nombre_couverts'].widget.attrs.update(
            {'placeholder': 'nombre de couverts'})
        self.fields['nombre_places'].widget.attrs.update(
            {'placeholder': 'nombre de places'})
        self.fields['nombre_cuisiniers'].widget.attrs.update(
            {'placeholder': 'nombre de cuisiniers'})
        self.fields['prix_moyen_couvert'].widget.attrs.update(
            {'placeholder': 'prix moyen'})

    def save(self, _user):
        """Create a new user"""
        super().save(commit=False)
        answer = GeneralIntroductionFormAnswer.objects.create(
            player=Player.objects.get(user=_user),
            metier=self.cleaned_data.get('metier'),
            ville=self.cleaned_data.get('ville'),
            age=self.cleaned_data.get('age'),
            experience=self.cleaned_data.get('experience'),
            nombre_couverts=self.cleaned_data.get('nombre_couverts'),
            nombre_places=self.cleaned_data.get('nombre_places'),
            nombre_cuisiniers=self.cleaned_data.get('nombre_cuisiniers'),
            prix_moyen_couvert=self.cleaned_data.get('prix_moyen_couvert'),
            nombre_etablissements=self.cleaned_data.get(
                'nombre_etablissements'),
        )
        return answer


class CarteForm(forms.ModelForm):
    class Meta:
        """Form options."""
        model = CarteFormAnswer
        fields = ['frequence_modification', 'rythme_trouve_suffisant', 'frequence_suggestion_du_jour', 'methode_calcul_de_prix',
                  'prix_trouve_justes_clients', 'prix_trouve_justes_soi']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update(
                {'class': 'default-input'})

    def save(self, _user):
        """Create a new user"""
        super().save(commit=False)
        answer = CarteFormAnswer.objects.create(
            player=Player.objects.get(user=_user),
            frequence_modification=self.cleaned_data.get(
                'frequence_modification'),
            rythme_trouve_suffisant=self.cleaned_data.get(
                'rythme_trouve_suffisant'),
            frequence_suggestion_du_jour=self.cleaned_data.get(
                'frequence_suggestion_du_jour'),
            methode_calcul_de_prix=self.cleaned_data.get(
                'methode_calcul_de_prix'),
            prix_trouve_justes_clients=self.cleaned_data.get(
                'prix_trouve_justes_clients'),
            prix_trouve_justes_soi=self.cleaned_data.get(
                'prix_trouve_justes_soi'),
        )
        return answer


class CreateEmptyUserForm(forms.ModelForm):
    class Meta:
        """Form options."""
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update(
                {'class': 'default-input'})
        self.fields['first_name'].widget.attrs.update(
            {'placeholder': 'Prénom'})
        self.fields['last_name'].widget.attrs.update(
            {'placeholder': 'Nom'})
        self.fields['email'].widget.attrs.update(
            {'placeholder': 'Email'})

    def save(self, password,sharing_code):
        """Create a new user"""
        super().save(commit=False)
        user = User.objects.create_user(
            email=self.cleaned_data.get('email'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            password=password,
            sharing_code = sharing_code
        )
        return user


class CreateEmptyPlayerForm(forms.ModelForm):
    class Meta:
        """Form options."""
        model = Player
        fields = ['restaurant_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['restaurant_name'].widget.attrs.update(
            {'class': 'default-input'})
        self.fields['restaurant_name'].widget.attrs.update(
            {'placeholder': 'Nom de votre restaurant'})

    def save(self, user):
        """Create a new player"""
        super().save(commit=False)
        player = Player.objects.create(
            user=user,
            restaurant_name=self.cleaned_data.get('restaurant_name'),
        )
        return player
