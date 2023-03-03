from django import forms
from form_and_game.forms import *
from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse
from form_and_game.helpers.autres_helpers import get_number_of_questions_with_autres_answers
from form_and_game.pointing_data import *
from django.contrib.auth.decorators import login_required
from form_and_game.helpers.helpers import send_recommendation_email

@login_required(login_url='register_player')
def first_slide(request):
    print( Player.objects.filter(user = request.user))   
    if (not Player.objects.filter(user = request.user).exists()):
        print("HERE")
        return redirect('register_player')
    request_player = Player.objects.get(user = request.user)
    if (GeneralIntroductionFormAnswer.objects.filter(player = request_player).exists()):
        return redirect('introduction_form_slide_02')
    else:
        if request.method == "POST":
            print(request.POST)
            form = GeneralInformationForm(request.POST)
            if form.is_valid():
                form.save(request.user)
                request_player.points = request_player.points + len(form.fields)*NUMBER_POINTS_PER_FIELD
                request_player.save()
                return redirect('introduction_form_slide_02')
            else:
                return render(request, 'form_elements/introduction_form/slide_01.html', {"title": "Enchanté!", "pages_seen_indicator": ".", "pages_left_indicator": "......", "form": form,"player":request_player,"progress_counter_display":"(1/7)"})
        form = GeneralInformationForm()
        print("created get form")
        return render(request, 'form_elements/introduction_form/slide_01.html', {"title": "Echanté!", "pages_seen_indicator": ".", "pages_left_indicator": "......", "form": form,"player":request_player,"progress_counter_display":"(1/7)"})



def second_slide(request):
    print("in first slide")
    request_player = Player.objects.get(user = request.user)
    if (not GeneralIntroductionFormAnswer.objects.filter(player = request_player).exists()):
        return redirect('introduction_form_slide_01')
    elif (CarteFormAnswer.objects.filter(player = request_player).exists()):
        return redirect('introduction_form_slide_03')
    else:
        if request.method == "POST":
            print(request.POST)
            form = CarteForm(request.POST)
            if form.is_valid():
                form.save(request.user)
                request_player.points = request_player.points + len(form.fields)*NUMBER_POINTS_PER_FIELD
                request_player.save()
                return redirect('introduction_form_slide_03')
            else:
                return render(request, 'form_elements/introduction_form/slide_02.html', {"title": "À la carte!", "pages_seen_indicator": "..", "pages_left_indicator": ".....", "form": form,"player":request_player,"progress_counter_display":"(2/7)"})
        form = CarteForm()
        print("created get form")
        return render(request, 'form_elements/introduction_form/slide_02.html', {"title": "À la carte!", "pages_seen_indicator": "..", "pages_left_indicator": ".....", "form": form,"player":request_player,"progress_counter_display":"(2/7)"})


def third_slide(request):
    request_player = Player.objects.get(user = request.user)
    if (not CarteFormAnswer.objects.filter(player = request_player).exists()):
        return redirect('introduction_form_slide_02')
    elif (RecetteFormAnswer.objects.filter(player = request_player).exists()):
        return redirect('introduction_form_slide_04')
    else:
        if request.method == "POST":
            print(request.POST)
            form = RecetteForm(request.POST)
            if form.is_valid():
                form.save(request.user)
                request_player.points = request_player.points + len(form.fields)*NUMBER_POINTS_PER_FIELD
                request_player.save()
                return redirect('introduction_form_slide_04')
            else:
                return render(request, 'form_elements/introduction_form/slide_03.html', {"title": "En cuisine!", "pages_seen_indicator": "...", "pages_left_indicator": "....", "form": form,"player":request_player,"progress_counter_display":"(3/7)"})
        form = RecetteForm()
        return render(request, 'form_elements/introduction_form/slide_03.html', {"title": "En cuisine!", "pages_seen_indicator": "...", "pages_left_indicator": "....", "form": form,"player":request_player,"progress_counter_display":"(3/7)"})


def fourth_slide(request):
    request_player = Player.objects.get(user = request.user)
    if (not RecetteFormAnswer.objects.filter(player = request_player).exists()):
        return redirect('introduction_form_slide_03')
    elif (CommandeFormAnswer.objects.filter(player = request_player).exists()):
        return redirect('introduction_form_slide_05')
    else:
        if request.method == "POST":
            print(request.POST)
            form = CommandeForm(request.POST)
            if form.is_valid():
                form.save(request.user)
                request_player.points = request_player.points + len(form.fields)*NUMBER_POINTS_PER_FIELD
                request_player.save()
                return redirect('introduction_form_slide_05')
            else:
                print(form.errors)
                return render(request, 'form_elements/introduction_form/slide_04.html', {"title": "Aux commandes!", "pages_seen_indicator": "....", "pages_left_indicator": "...", "form": form,"player":request_player,"progress_counter_display":"(4/7)"})
        form = CommandeForm()
        return render(request, 'form_elements/introduction_form/slide_04.html', {"title": "Aux commandes!", "pages_seen_indicator": "....", "pages_left_indicator": "...", "form": form,"player":request_player,"progress_counter_display":"(4/7)"})


def fifth_slide(request):
    request_player = Player.objects.get(user = request.user)
    if (not CommandeFormAnswer.objects.filter(player = request_player).exists()):
        return redirect('introduction_form_slide_04')
    elif (ConnaissanceAchatFormAnswer.objects.filter(player = request_player).exists()):
        return redirect('introduction_form_slide_06')
    else:
        if request.method == "POST":
            print(request.POST)
            form = ConnaissanceAchatForm(request.POST)
            if form.is_valid():
                form.save(request.user)
                request_player.points = request_player.points + len(form.fields)*NUMBER_POINTS_PER_FIELD
                request_player.save()
                return redirect('introduction_form_slide_06')
            else:
                return render(request, 'form_elements/introduction_form/slide_05.html', {"title": "De bonne facture!", "pages_seen_indicator": ".....", "pages_left_indicator": "..", "form": form,"player":request_player,"progress_counter_display":"(5/7)"})
        form = ConnaissanceAchatForm()
        return render(request, 'form_elements/introduction_form/slide_05.html', {"title": "De bonne facture!", "pages_seen_indicator": ".....", "pages_left_indicator": "..", "form": form,"player":request_player,"progress_counter_display":"(5/7)"})


def sixth_slide(request):
    request_player = Player.objects.get(user = request.user)
    if (not ConnaissanceAchatFormAnswer.objects.filter(player = request_player).exists()):
        return redirect('introduction_form_slide_05')
    elif (ComptaFormAnswer.objects.filter(player = request_player).exists()):
        return redirect('introduction_form_slide_07')
    if request.method == "POST":
        print(request.POST)
        form = ComptaForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            request_player.points = request_player.points + len(form.fields)*NUMBER_POINTS_PER_FIELD
            request_player.save()
            return redirect('introduction_form_slide_07')
        else:
            return render(request, 'form_elements/introduction_form/slide_06.html', {"title": "Parlons chiffres!", "pages_seen_indicator": "......", "pages_left_indicator": ".", "form": form,"player":request_player,"progress_counter_display":"(6/7)"})
    form = ComptaForm()
    return render(request, 'form_elements/introduction_form/slide_06.html', {"title": "Parlons chiffres!", "pages_seen_indicator": "......", "pages_left_indicator": ".", "form": form,"player":request_player,"progress_counter_display":"(6/7)"})

def seventh_slide(request):
    request_player = Player.objects.get(user = request.user)
    if (not ComptaFormAnswer.objects.filter(player = request_player).exists()):
        return redirect('introduction_form_slide_06')
    elif (FonctionnalitesPrefereesFormAnswer.objects.filter(player = request_player).exists()):
        return redirect('introduction_form_conclusion_slide')
    else:
        if request.method == "POST":
            print(request.POST)
            form = FonctionnalitesPrefereesForm(request.POST)
            if form.is_valid():
                form.save(request.user)
                request_player.points = request_player.points + len(form.fields)*NUMBER_POINTS_PER_FIELD
                request_player.save()
                return redirect('introduction_form_conclusion_slide')
            else:
                return render(request, 'form_elements/introduction_form/slide_07.html', {"title": "Rien que pour vous", "pages_seen_indicator": ".......", "pages_left_indicator": "", "form": form,"player":request_player,"progress_counter_display":"(7/7)"})
        form = FonctionnalitesPrefereesForm()
        return render(request, 'form_elements/introduction_form/slide_07.html', {"title": "Rien que pour vous", "pages_seen_indicator": ".......", "pages_left_indicator": "", "form": form,"player":request_player,"progress_counter_display":"(7/7)"})

def conclusion_slide(request):
    request_player = Player.objects.get(user = request.user)
    url_to_copy = f"{request.build_absolute_uri(reverse('register_player'))}{request.user.sharing_code}"
    if (not FonctionnalitesPrefereesFormAnswer.objects.filter(player = request_player).exists()):
        return redirect('introduction_form_slide_06')
    if not request_player.was_added_precision_points:
        print("TRYING IT")
        number_autres = get_number_of_questions_with_autres_answers(request_player)
        print(f"NUMBER AUTRES {number_autres}")
        request_player.points = request_player.points + (MAXIMUM_NUMBER_OF_AUTRES_ANSWERS-number_autres)*NUMBER_POINTS_PER_NON_AUTRES_FIELDS
        print(f"ADDED {(MAXIMUM_NUMBER_OF_AUTRES_ANSWERS-number_autres)*NUMBER_POINTS_PER_NON_AUTRES_FIELDS}")
        if number_autres == 0:
            request_player.needs_precising = False
        request_player.was_added_precision_points = True
        print(f"SAVED")
        request_player.save()
    if request.method=="POST":
        if request.POST.get('rappel'):
            if not request_player.to_contact_when_product_is_out:
                request_player.to_contact_when_product_is_out = True
                request_player.save()
                messages.add_message(request, messages.SUCCESS, "Merci pour votre confiance! Nous sommes ravi de vous accueillir dans notre famille et vous contacterons dès que le produit sera prêt.")
            else:
                messages.add_message(request, messages.SUCCESS, "On adore votre enthousiasme! Vous êtes déjà sur la précieuse liste.")
        elif request.POST.get('jouer'):
            return redirect('game_home')
        elif request.POST.get("send_email") and request.POST.get("email"):
            send_recommendation_email(request.user,request.POST.get("email"),url_to_copy)
    return render(request,'form_elements/introduction_form/conclusion_slide.html',{"title": "🥳 Merci!","player":request_player,"player_classement":"30ème","url_to_copy":url_to_copy})