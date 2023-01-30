from django import forms
from form_and_game.models import *


class GeneralInformationForm(forms.ModelForm):
    class Meta:
        """Form options."""
        model = GeneralIntroductionFormAnswer
        fields = ['metier', 'ville', 'age', 'nombre_couverts',
                  'nombre_cuisiniers', 'prix_moyen_assiette', 'nombre_etablissements', 'experience', 'nombre_places']

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
        self.fields['prix_moyen_assiette'].widget.attrs.update(
            {'placeholder': 'prix moyen'})
