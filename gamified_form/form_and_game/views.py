from django.shortcuts import render
from form_and_game.forms import *
from django.contrib.auth import authenticate, login, logout
from form_and_game.helpers.helpers import *
from django.shortcuts import redirect, render
from form_and_game.helpers.decorators import login_prohibited, allowed_groups
from django.contrib.auth.decorators import login_required
from form_and_game.form_functions import introduction_form_functions
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail
from form_and_game.helpers.autres_helpers import get_list_of_questions_from_autre_answers,handle_autres_post_request,get_number_of_questions_with_autres_answers
from form_and_game.pointing_data import NUMBER_POINTS_PER_NON_AUTRES_FIELDS
from django.http import HttpResponseRedirect
import csv
from django.http import HttpResponse
from form_and_game.helpers.file_responses_generator import *
# Create your views here.

@login_prohibited
def register_player(request,sharer_code=""):
    if request.method == "POST":
        if request.POST.get("restaurant_name") and request.POST.get("first_name") and request.POST.get("last_name") and request.POST.get("email"):
            user_register_form = CreateEmptyUserForm(request.POST)
            player_register_form = CreateEmptyPlayerForm(request.POST)
            if user_register_form.is_valid() and player_register_form.is_valid():
                random_password = create_random_password(12)
                sharing_code = create_share_code()
                created_user = user_register_form.save(random_password,sharing_code)
                player = player_register_form.save(created_user)
                user = authenticate(email=created_user.email,
                                    password=random_password)
                if user is not None:
                    login(request, user)
                if sharer_code:
                    recommender = User.objects.get(sharing_code = sharer_code)
                    if recommender.is_administrator():
                        player.is_validated = True
                        player.save()
                    else:
                        recommender_player = Player.objects.get(user = recommender)
                        recommender_player.points = recommender_player.points + 100
                        recommender_player.save()
                        SharingAlert.objects.create(user = recommender,text=f"{user.full_name_no_comma()} a accepté votre invitation. Vous avez gagné 100 points!")
                return redirect('introduction_form')
            else:
                messages.add_message(request, messages.ERROR, "Merci de vérifier la validité des champs renseignés, notamment de votre adresse email.")
                return render(request, 'form_elements/player_register/register_slide.html', {"title": "😊 Bienvenue, chef!", "user_register_form": user_register_form, "player_register_form": player_register_form})
        else:
            print("ERROR")

    user_register_form = CreateEmptyUserForm()
    player_register_form = CreateEmptyPlayerForm()
    return render(request, 'form_elements/player_register/register_slide.html', {"title": "😊 Bienvenue, chef!", "user_register_form": user_register_form, "player_register_form": player_register_form})

@login_required
def game_home(request):
    request_player = Player.objects.get(user = request.user)
    if not FonctionnalitesPrefereesFormAnswer.objects.filter(player=request_player).exists():
        return redirect('introduction_form')
    new_successful_sharings = SharingAlert.objects.filter(user=request.user,was_shared=False)
    user_sharing_url = f"{request.build_absolute_uri(reverse('register_player'))}{request.user.sharing_code}"
    if new_successful_sharings:
        for sharing in new_successful_sharings:
            messages.add_message(request, messages.SUCCESS, sharing.text)
            sharing.was_shared = True
            sharing.save()
    ranking = get_ranking()
    ranking_to_display = get_ranking_to_display(ranking,request.user)
    points_to_gain_a_spot = get_points_to_person_before(ranking,request.user) +1 
    points_to_win = get_points_to_top_five(ranking,request.user) +1
    try:
        show_extra_info = not ranking_to_display[0]['is_user']
    except:
        show_extra_info = True
    request_player = Player.objects.get(user = request.user)
    if request.method == "POST":
        if request.POST.get("change_mdp"):
            if (request.POST.get("password") and request.POST.get("confirmation") and request.POST.get("accept_conditions")):
                if (request.POST.get("password") == request.POST.get("confirmation")):
                    request.user.set_password(request.POST.get("password"))
                    request.user.accepted_conditions = True
                    request.user.save()
                    user = authenticate(email=request.user.email,
                                    password=request.POST.get("password"))
                    login(request, user)
                    messages.add_message(request, messages.SUCCESS, "Bienvenue dans la partie! Votre mot de passe a bien été changé.")
                else:
                    return render(request, 'main_game_page.html',{"show_extra_info":show_extra_info,"ranking":ranking_to_display,"player":request_player,"points_to_gain_a_spot":points_to_gain_a_spot,"points_to_win":points_to_win,"mdp_error":"La confirmation diffère du mot de passe.","has_to_change_pwd":True,"url_to_copy":user_sharing_url})
        elif request.POST.get("log_out"):
            return redirect('log_out')
        elif request.POST.get("precise_answers"):
            return redirect("autres_form")
        elif request.POST.get("schedule_call"):
            CallDemand.objects.create(player=request_player)
            return redirect("https://calendly.com/a-sirgue/discussion-cuisine")
        elif request.POST.get("conditions"):
            return redirect('conditions_generales')
        elif request.POST.get("send_email") and request.POST.get("email"):
            send_recommendation_email(request.user,request.POST.get("email"),user_sharing_url)
    number_of_autres_fields=get_number_of_questions_with_autres_answers(request_player)
    points_possible_by_removing_autres = number_of_autres_fields*NUMBER_POINTS_PER_NON_AUTRES_FIELDS
    time_needed_to_remove_autres = number_of_autres_fields/6.0
    if time_needed_to_remove_autres<1:
        time_needed_to_remove_autres = str(int(time_needed_to_remove_autres*60))+" sec."
    else:
        time_needed_to_remove_autres = str(int(time_needed_to_remove_autres))+" min."
    return render(request, 'main_game_page.html',{"show_extra_info":show_extra_info,"ranking":ranking_to_display,"player":request_player,"points_to_gain_a_spot":points_to_gain_a_spot,"points_to_win":points_to_win,"has_to_change_pwd":not request.user.accepted_conditions,"url_to_copy":user_sharing_url,"number_of_points_with_autres_form":points_possible_by_removing_autres,"time_for_autres_form":time_needed_to_remove_autres})


def log_out(request):
    logout(request)
    return redirect('log_in')

@login_prohibited
def log_in(request):
    if request.method == 'POST':
        if request.POST.get("create_account"):
            return redirect('register_player')
        else:
            form = LogInForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')
                user = authenticate(email=email, password=password)
                if user is not None:
                    login(request, user)
                    if user.is_administrator():
                        redirect_url = request.POST.get('next') or 'admin_page'
                    else:
                        redirect_url = request.POST.get('next') or 'game_home'
                    return redirect(redirect_url)
            messages.add_message(request, messages.ERROR,
                                "Email ou mot de passe erronné.")
    form = LogInForm()
    next = request.GET.get('next') or ''
    return render(request, 'log_in.html', {'form': form, 'next': next})
   

@login_required(login_url='register_player')
def introduction_form(request):
    if Player.objects.filter(user = request.user).exists():
            request_player = Player.objects.get(user = request.user)
            if (FonctionnalitesPrefereesFormAnswer.objects.filter(player = request_player).exists()):
                return redirect("game_home")
            elif (ComptaFormAnswer.objects.filter(player = request_player).exists()):
                return redirect("introduction_form_slide_06")
            elif (ConnaissanceAchatFormAnswer.objects.filter(player = request_player).exists()):
                return redirect("introduction_form_slide_05")
            elif (CommandeFormAnswer.objects.filter(player = request_player).exists()):
                return redirect("introduction_form_slide_04")
            elif (RecetteFormAnswer.objects.filter(player = request_player).exists()):
                return redirect("introduction_form_slide_03")
            elif (CarteFormAnswer.objects.filter(player = request_player).exists()):
                return redirect("introduction_form_slide_02")
            else:
                return redirect("introduction_form_slide_01")
    else:
        return redirect("register_player")

@login_required
def autres_form(request):
    request_player = Player.objects.get(user=request.user)
    if request.method=="POST":
        if request.POST.get("quit"):
            return redirect('game_home')
        else:
            handle_autres_post_request(request,request_player)
    questions = get_list_of_questions_from_autre_answers(request_player)
    if not questions:
        request_player.needs_precising = False
        request_player.save()
        return redirect('game_home')
    if questions:
        return render(request,"form_elements/autres_form/autres_form.html",{"questions":questions,"player":request_player})

@login_required
def conditions_generales(request):
    if request.method=="POST":
        if request.POST.get("quit"):
            return redirect('game_home')
        elif request.POST.get("contact"):
            return HttpResponseRedirect("mailto:hello.cuisine@outlook.com?subject=Demande Conditions Générales d'Utilisation")
    request_player = Player.objects.get(user=request.user)
    return render(request,"cgv.html",{"player":request_player})

@login_required
@allowed_groups(["Administrator"])
def admin_page(request):
    number_users = Player.objects.all().count() - 20
    number_shares = SharingAlert.objects.all().count()
    number_calls_demanded = CallDemand.objects.all().count()
    average_value = get_average_value_awarded_to_our_product()
    most_looked_for_features = get_most_liked_features()  
    user_sharing_url = f"{request.build_absolute_uri(reverse('register_player'))}{request.user.sharing_code}"
    if request.method=="POST":
        if request.POST.get("go_admin"):
            return redirect("/admin")
        elif request.POST.get("quit"):
            return redirect('log_out')
        elif request.POST.get("flexRadioDefault"):
            if request.POST.get("flexRadioDefault") == "all_users":
                return generate_user_data_csv_response()
            elif request.POST.get("flexRadioDefault") == "all_data":
                return generate_all_answer_data_csv_response()
            elif request.POST.get("flexRadioDefault") == "all_extra_info":
                return generate_extra_info_data_csv_response()
        
    return render(request,'admin_home.html',{"url_to_share":user_sharing_url,"number_users":number_users,"number_shares":number_shares,"number_calls_demanded":number_calls_demanded,"average_value":average_value,"most_looked_for_features":most_looked_for_features})
            

def error_404(request,exception):
    if request.method =="POST":
        return redirect('game_home')
    return render(request,'error_404.html')