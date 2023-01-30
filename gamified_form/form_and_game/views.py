from django.shortcuts import render
from form_and_game.forms import *
# Create your views here.


def general_design(request):
    form = GeneralInformationForm()
    return render(request, 'form_elements/introduction_form/slide_01.html', {"title": "Enchanté!", "pages_seen_indicator": ".", "pages_left_indicator": ".........", "form": form})
