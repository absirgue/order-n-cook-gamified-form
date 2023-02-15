from form_and_game.models import *
from form_and_game.pointing_data import NUMBER_POINTS_PER_NON_AUTRES_FIELDS

def get_number_of_questions_with_autres_answers(player):
    length = 0
    autres_questions = get_list_of_questions_from_autre_answers(player)
    for question in autres_questions:
        length += len(question['questions'])
    return length

def get_list_of_questions_from_autre_answers(player):
    list_of_autres_field = []
    if get_list_of_autres_carte_form(player):
        list_of_autres_field.append(get_list_of_autres_carte_form(player))
    if get_list_of_autres_compta_form(player):
        list_of_autres_field.append(get_list_of_autres_compta_form(player))
    if get_list_of_autres_commande_form(player):
        list_of_autres_field.append(get_list_of_autres_commande_form(player))
    if get_list_of_autres_connaissance_achat_form(player):
        list_of_autres_field.append(get_list_of_autres_connaissance_achat_form(player))
    if get_list_of_autres_recette_form(player):
        list_of_autres_field.append(get_list_of_autres_recette_form(player))
    return list_of_autres_field


def get_list_of_autres_compta_form(player):
    result = []
    if ComptaFormAnswer.objects.filter(player=player).exists():
        form = ComptaFormAnswer.objects.get(player=player)
        if form.moyen_obtention_coefficients == "Autre" and not ExtraInformation.objects.filter(player=player).filter(field_title="moyen_obtention_coefficients").exists():
            result.append({"question_title":"moyen_obtention_coefficients","question":"Pouvez-vous nous expliquer comment vous calculez et consultez votre marge et votre coefficient actuellement?"})
        if form.frequence_connaissance_coefficient == "Autre" and not ExtraInformation.objects.filter(player=player).filter(field_title="frequence_connaissance_coefficient").exists():
            result.append({"question_title":"frequence_connaissance_coefficient","question":"À quelle fréquence pouvez-vous consulter votre marge et votre coefficient actuellement?"})
        if form.unite_cout_optention_bilan == "Autre" and not ExtraInformation.objects.filter(player=player).filter(field_title="unite_cout_optention_bilan").exists():
            result.append({"question_title":"unite_cout_optention_bilan","question":"Comment vous est tariffée l'obtention de votre marge et de votre coefficient (de votre bilan comptable)?"})
        if result:
            return {"title":"Comptabilité","questions":result}

def get_list_of_autres_connaissance_achat_form(player):
    result = []
    if ConnaissanceAchatFormAnswer.objects.filter(player=player).exists():
        form = ConnaissanceAchatFormAnswer.objects.get(player=player)
        if form.methode_validation_paiement == "Autre" and not ExtraInformation.objects.filter(player=player).filter(field_title="methode_validation_paiement").exists():
            result.append({"question_title":"methode_validation_paiement","question":"Quel système avez-vous pour mémoriser le bon paiment des factures?"})
        if form.connaissance_moyenne_chiffree_des_achats == "Autre" and not ExtraInformation.objects.filter(player=player).filter(field_title="connaissance_moyenne_chiffree_des_achats").exists():
            result.append({"question_title":"connaissance_moyenne_chiffree_des_achats","question":"Quelles statistiques arrivez-vous à obtenir sur vos achats (coût total, répartition par catégorie, par fournisseur,...)?"})
        if result:
            return {"title":"Connaissance des achats","questions":result}

def get_list_of_autres_commande_form(player):
    result = []
    if CommandeFormAnswer.objects.filter(player=player).exists():
        form = CommandeFormAnswer.objects.get(player=player)
        if form.methode_passage_commande == "Autre" and not ExtraInformation.objects.filter(player=player).filter(field_title="methode_passage_commande").exists():
            result.append({"question_title":"methode_passage_commande","question":"Comment passez-vous vos commandes?"})
        if form.frequence_passage_commande == "Autre" and not ExtraInformation.objects.filter(player=player).filter(field_title="frequence_passage_commande").exists():
            result.append({"question_title":"frequence_passage_commande","question":"À quelle fréquence passez-vous commande?"})
        if form.support_memorisation == "Autre" and not ExtraInformation.objects.filter(player=player).filter(field_title="support_memorisation").exists():
            result.append({"question_title":"support_memorisation","question":"Comment mémorisez-vous vos commandes?"})
        if form.methode_classement_commandes == "Autre" and not ExtraInformation.objects.filter(player=player).filter(field_title="methode_classement_commandes").exists():
            result.append({"question_title":"methode_classement_commandes","question":"Comment classez-vous vos commandes passées?"})
        if form.methode_classement_bons_livraison == "Autre" and not ExtraInformation.objects.filter(player=player).filter(field_title="methode_classement_bons_livraison").exists():
            result.append({"question_title":"methode_classement_bons_livraison","question":"Comment classez-vous vos bons de livraison passés?"})
        if form.methode_classement_factures == "Autre" and not ExtraInformation.objects.filter(player=player).filter(field_title="methode_classement_factures").exists():
            result.append({"question_title":"methode_classement_factures","question":"Comment classez-vous vos factures?"})
        if form.methode_transmission_facture == "Autre" and not ExtraInformation.objects.filter(player=player).filter(field_title="methode_transmission_facture").exists():
            result.append({"question_title":"methode_transmission_facture","question":"Comment transmettez-vous vos factures à votre comptabilité?"})
        if result:
            return {"title":"Passage de commandes","questions":result}

def get_list_of_autres_recette_form(player):
    result = []
    if RecetteFormAnswer.objects.filter(player=player).exists():
        form = RecetteFormAnswer.objects.get(player=player)
        if form.support_memorisation == "Autre" and not ExtraInformation.objects.filter(player=player).filter(field_title="support_memorisation").exists():
            result.append({"question_title":"support_memorisation","question":"Quel est votre système pour mémoriser vos recettes?"})
        if form.methode_transmission_savoir == "Autre" and not ExtraInformation.objects.filter(player=player).filter(field_title="methode_transmission_savoir").exists():
            result.append({"question_title":"methode_transmission_savoir","question":"Comment transmettez-vous votre savoir au sein de votre restaurant?"})
        if result:
            return {"title":"Gestion des recettes","questions":result}

def get_list_of_autres_carte_form(player):
    result = []
    if CarteFormAnswer.objects.filter(player=player).exists():
        form = CarteFormAnswer.objects.get(player=player)
        if form.frequence_modification == "Autre" and not ExtraInformation.objects.filter(player=player).filter(field_title="frequence_modification").exists():
            result.append({"question_title":"frequence_modification","question":"À quelle fréquence modifiez-vous votre carte?"})
        if form.frequence_suggestion_du_jour == "Autre" and not ExtraInformation.objects.filter(player=player).filter(field_title="frequence_suggestion_du_jour").exists():
            result.append({"question_title":"frequence_suggestion_du_jour","question":"À quelle fréquence changez-vous les suggestions du jour?"})
        if form.methode_calcul_de_prix == "Autre" and not ExtraInformation.objects.filter(player=player).filter(field_title="methode_calcul_de_prix").exists():
            result.append({"question_title":"methode_calcul_de_prix","question":"Comment calculez-vous le prix de vente de vos plats aujourd'hui?"})
        if result:
            return {"title":"Votre carte","questions":result}

def handle_autres_post_request(request, player):
    if request.POST.get('Votre carte'):
        fields = ["frequence_modification","frequence_suggestion_du_jour","methode_calcul_de_prix"]
        for field in fields:
            if request.POST.get(field):
                ExtraInformation.objects.create(player=player,field_title=field,answer=request.POST.get(field))
                add_precision_points(player)
    elif request.POST.get('Gestion des recettes'):
        fields = ["support_memorisation","methode_transmission_savoir"]
        for field in fields:
            if request.POST.get(field):
                ExtraInformation.objects.create(player=player,field_title=field,answer=request.POST.get(field))
                add_precision_points(player)
    elif request.POST.get('Passage de commandes'):
        fields = ["methode_passage_commande","frequence_passage_commande","support_memorisation","methode_classement_commandes","methode_classement_bons_livraison","methode_classement_factures","methode_transmission_facture"]
        for field in fields:
            if request.POST.get(field):
                ExtraInformation.objects.create(player=player,field_title=field,answer=request.POST.get(field))
                add_precision_points(player)
    elif request.POST.get('Connaissance des achats'):
        fields = ["methode_validation_paiement","connaissance_moyenne_chiffree_des_achats"]
        for field in fields:
            if request.POST.get(field):
                ExtraInformation.objects.create(player=player,field_title=field,answer=request.POST.get(field))
                add_precision_points(player)
    elif request.POST.get('Comptabilité'):
        fields = ["moyen_obtention_coefficients","frequence_connaissance_coefficient","unite_cout_optention_bilan"]
        for field in fields:
            if request.POST.get(field):
                ExtraInformation.objects.create(player=player,field_title=field,answer=request.POST.get(field))
                add_precision_points(player)

def add_precision_points(player):
    player.points = player.points + NUMBER_POINTS_PER_NON_AUTRES_FIELDS
    player.save()
