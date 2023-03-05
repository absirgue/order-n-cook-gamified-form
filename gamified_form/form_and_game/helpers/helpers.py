from random import sample
from secrets import choice
from string import *
from form_and_game.models import GeneralIntroductionFormAnswer, Player,User,ComptaFormAnswer,FonctionnalitesPrefereesFormAnswer
import uuid
from django.core.mail import send_mail
from django.conf import settings


def create_random_password(length):
    alphabet = ascii_letters + digits + punctuation
    requirements = [ascii_uppercase,        # at least one uppercase letter
                    ascii_lowercase,        # at least one lowercase letter
                    digits,                 # at least one digit
                    punctuation,            # at least one symbol
                    *(length-4)*[alphabet]]  # rest: letters digits and symbols
    return "".join(choice(req) for req in sample(requirements, length))

def create_share_code():
    return str(uuid.uuid4())

def get_ranking():
    players = Player.objects.all().order_by('-points')
    result = []
    for i in range(len(players)):
        player = players[i]
        rank=i+1
        rank_indicator = ""
        if rank == 1:
            rank_indicator = "🥇"
        elif rank ==2:
            rank_indicator = "🥈"
        elif rank==3:
            rank_indicator = "🥉"
        elif rank==4:
            rank_indicator = "4️⃣"
        elif rank==5:
            rank_indicator = "5️⃣"
        else:
            rank_indicator = str(rank)
        try:
            player_info = {"id":player.user_id,"first_name":' '.join(elem.capitalize() for elem in player.user.first_name.split()),"city":GeneralIntroductionFormAnswer.objects.get(player=player).ville,"points":player.points,"rank_symbol":rank_indicator,"rank":rank}
        except Exception as e:
            player_info = {"id":player.user_id,"first_name":' '.join(elem.capitalize() for elem in player.user.first_name.split()),"city":"","points":player.points,"rank_symbol":rank_indicator,"rank":rank}
        result.append(player_info)
    return result

def get_ranking_to_display(ranking,user):
    request_player_ranking = 0
    for item in ranking:
        if item["id"] == user.id:
            request_player_ranking = item["rank"]
            item["is_user"] = True
    if request_player_ranking <= 13:
        list = ranking[:13]
        list.append({"represents_multiple":True})
        return list
    elif request_player_ranking >= 13:
        list = ranking[:5]
        list.append({"represents_multiple":True})
        if len(ranking) >= request_player_ranking+3:
            for i in range(request_player_ranking-3,request_player_ranking+4):
                list.append(ranking[i])
            list.append({"represents_multiple":True})
        else:
            for i in range(request_player_ranking-7,len(ranking)):
                list.append(ranking[i])
        return list

def get_points_to_person_before(ranking,user):
    request_player_idx = get_index_of_user_in_ranking(ranking,user)
    if request_player_idx >0:
        return ranking[request_player_idx-1]["points"] - ranking[request_player_idx]["points"]
    else:
        return 0 

def get_points_to_top_five(ranking,user):
    request_player_idx = get_index_of_user_in_ranking(ranking,user)
    if request_player_idx<=4:
        return 0
    return ranking[4]["points"] - ranking[request_player_idx]["points"]

def get_index_of_user_in_ranking(ranking,user):
    for i in range(len(ranking)):
        if ranking[i]["id"] == user.id:
            return i
    
def send_recommendation_email(author,recipient_email_address,link):
    send_mail(
        subject=f"{author.first_name} vous invite chez Order n'Cook!",
        message=f"👋Bonjour,\n\n {author.full_name_no_comma()} vous invite à rejoindre le jeu exceptionnel de Order n'Cook!\n\n😊Un peu de contexte: chez Order n'Cook, on développe l'outil de référence pour les restaurateur comme toi. Gestion des commandes, mémorisation des recettes, relations fournisseurs, analyse de la marge et du coefficient en temps réel, et plus encore ... tout est sur Order n'Cook! \n🥇Alors, depuis quelques mois, de nombreux chefs participent à notre jeu exceptionnel pour gagner un accès à notre plateforme.\n\nPour participer (et tenter de doubler {author.first_name}), cliquez sur ce lien: {link}\n\nBonne partie et à bientôt sur Order n'Cook!\nÉric et Anton\nFondateurs\n\n\nPS: on est super sympa alors n'hésite pas à répondre à cet email pour toute question ou demande :)",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[recipient_email_address])
    
def get_average_value_awarded_to_our_product():
    records = ComptaFormAnswer.objects.all()
    total = 0
    count = 0
    for record in records:
        total += record.depense_consentie_notre_version
        count +=1
    if count > 0:
        return round(total/count,2)
    else: 
        return '-' 

def get_most_liked_features():
    records = FonctionnalitesPrefereesFormAnswer.objects.all()
    options_and_score = {}
    for record in records:
        if record.premiere_fonctionnalite in options_and_score:
            options_and_score[record.premiere_fonctionnalite] += 3
        else:
            options_and_score[record.premiere_fonctionnalite] = 3
        if record.deuxieme_fonctionnalite in options_and_score:
            options_and_score[record.deuxieme_fonctionnalite] += 2
        else:
            options_and_score[record.deuxieme_fonctionnalite] = 2
        if record.troisieme_fonctionnalite in options_and_score:
            options_and_score[record.troisieme_fonctionnalite] += 1
        else:
            options_and_score[record.troisieme_fonctionnalite] = 1
    maximums = []
    if len(options_and_score) >=1:
        max_value = max(options_and_score, key=options_and_score.get)
        maximums.append({"name":max_value,"points":options_and_score[max_value],"rank":1})
        del options_and_score[max_value]
        if len(options_and_score) >=1:
            max_value = max(options_and_score, key=options_and_score.get)
            maximums.append({"name":max_value,"points":options_and_score[max_value],"rank":2})
            del options_and_score[max_value]
        if len(options_and_score) >=1:
            max_value = max(options_and_score, key=options_and_score.get)
            maximums.append({"name":max_value,"points":options_and_score[max_value],"rank":3})
            del options_and_score[max_value]
            if len(options_and_score) >=1:
                max_value = max(options_and_score, key=options_and_score.get)
                maximums.append({"name":max_value,"points":options_and_score[max_value],"rank":4})
    return maximums