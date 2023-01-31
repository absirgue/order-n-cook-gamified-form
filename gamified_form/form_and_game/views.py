from django.shortcuts import render
from form_and_game.forms import *
from django.contrib.auth import authenticate, login, logout
from form_and_game.helpers.helpers import createRandomPassword
from django.shortcuts import redirect, render
from form_and_game.helpers.decorators import login_prohibited, allowed_groups
from django.contrib.auth.decorators import login_required
# Create your views here.


def register_player(request):
    if request.method == "POST":
        if request.POST.get("restaurant_name") and request.POST.get("first_name") and request.POST.get("last_name") and request.POST.get("email"):
            user_register_form = CreateEmptyUserForm(request.POST)
            player_register_form = CreateEmptyPlayerForm(request.POST)
            if user_register_form.is_valid() and player_register_form.is_valid():
                random_password = createRandomPassword(12)
                created_user = user_register_form.save(random_password)
                player_register_form.save(created_user)
                user = authenticate(email=created_user.email,
                                    password=random_password)
                if user is not None:
                    login(request, user)
                return redirect('general_for_now')
            else:
                print("NOT VALID")
        else:
            print("ERROR")
            # GIVE A MESSAGE

    user_register_form = CreateEmptyUserForm()
    player_register_form = CreateEmptyPlayerForm()
    return render(request, 'form_elements/player_register/register_slide.html', {"title": "😊 Bievenue, chef!", "user_register_form": user_register_form, "player_register_form": player_register_form})


def log_out(request):
    logout(request)
    return redirect('log_in')


def log_in(request):
    print("Not done")


def general_design(request):
    if request.method == "POST":
        print(request.POST)
        form = GeneralInformationForm(request.POST)
        if form.is_valid():
            form.save(request.user)
        else:
            print("NOT VALID")
            print(form.errors())
    form = GeneralInformationForm()
    return render(request, 'form_elements/introduction_form/slide_01.html', {"title": "Enchanté!", "pages_seen_indicator": ".", "pages_left_indicator": ".........", "form": form})


def second_slide(request):
    if request.method == "POST":
        print(request.POST)
        form = CarteForm(request.POST)
        if form.is_valid():
            form.save(request.user)
        else:
            print("NOT VALID")
            print(form.errors())
    form = CarteForm()
    return render(request, 'form_elements/introduction_form/slide_02.html', {"title": "À la carte!", "pages_seen_indicator": "..", "pages_left_indicator": "........", "form": form})


def third_slide(request):
    if request.method == "POST":
        print(request.POST)
        form = RecetteForm(request.POST)
        if form.is_valid():
            form.save(request.user)
        else:
            print("NOT VALID")
            print(form.errors())
    form = RecetteForm()
    return render(request, 'form_elements/introduction_form/slide_03.html', {"title": "En cuisine!", "pages_seen_indicator": "...", "pages_left_indicator": ".......", "form": form})


def fourth_slide(request):
    if request.method == "POST":
        print(request.POST)
        form = CommandeForm(request.POST)
        if form.is_valid():
            form.save(request.user)
        else:
            print("NOT VALID")
            print(form.errors())
    form = CommandeForm()
    return render(request, 'form_elements/introduction_form/slide_04.html', {"title": "Aux commandes!", "pages_seen_indicator": "....", "pages_left_indicator": "......", "form": form})


def fifth_slide(request):
    if request.method == "POST":
        print(request.POST)
        form = ConnaissanceAchatForm(request.POST)
        if form.is_valid():
            form.save(request.user)
        else:
            print("NOT VALID")
            print(form.errors())
    form = ConnaissanceAchatForm()
    return render(request, 'form_elements/introduction_form/slide_05.html', {"title": "De bonne facture!", "pages_seen_indicator": ".....", "pages_left_indicator": ".....", "form": form})


def sixth_slide(request):
    if request.method == "POST":
        print(request.POST)
        form = ComptaForm(request.POST)
        if form.is_valid():
            form.save(request.user)
        else:
            print("NOT VALID")
            print(form.errors())
    form = ComptaForm()
    return render(request, 'form_elements/introduction_form/slide_06.html', {"title": "Parlons chiffres!", "pages_seen_indicator": "......", "pages_left_indicator": "....", "form": form})
