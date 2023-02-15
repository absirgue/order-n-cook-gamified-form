import csv
from django.http import HttpResponse
from form_and_game.models import * 

def generate_user_data_csv_response():
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="order_n_cook_tous_utilisateurs.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow(['ID', 'Prénom', 'Nom', 'Email',"Numero de telephone","Ville","Nom de l'etablissement","A contacter à la sortie du produit?","A ete valide","Nb points","Statut","A accepte les conditions d'utilisation",])
    users = User.objects.all()
    for user in users:
        if not (user.is_staff or user.is_superuser or user.randomly_created):
            try:
                player = Player.objects.get(user = user)
                general_info = GeneralIntroductionFormAnswer.objects.get(player=player)
                writer.writerow([user.id, user.first_name, user.last_name,user.email,f"{value_or_blank_value(player.phone_number)}", f"{value_or_blank_value(general_info.ville)}",f"{value_or_blank_value(player.restaurant_name)}",f"{value_or_blank_value(player.to_contact_when_product_is_out)}",f"{value_or_blank_value(player.is_validated)}",f"{value_or_blank_value(player.points)}",f"{value_or_blank_value(player.get_status_name())}",f"{value_or_blank_value(user.accepted_conditions)}"])
            except Exception as e:
                    print(e)
                    writer.writerow([f"ERROR READING {user.full_name()}"])
    return response

def generate_extra_info_data_csv_response():
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="order_n_cook_precisions.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow(['Auteur', 'Question', 'Reponse'])
    extra_info_records = ExtraInformation.objects.all().order_by("field_title")
    for extra_info in extra_info_records:
        try:
            writer.writerow([f"{value_or_blank_value(extra_info.player.user.full_name())}", f"{value_or_blank_value(extra_info.field_title)}",f"{value_or_blank_value(extra_info.answer)}"])
        except Exception as e:
            print(e)
            writer.writerow(["ERROR READING"])
    return response


def generate_all_answer_data_csv_response():
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="order-n_cook_toutes_reponses_et_auteurs.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow(['Nom, Prenom', "Valide?",'[CARTE] Frequence Modification', '[CARTE] Frequence Trouvee Suffisante?', '[CARTE] Frequence Changement Suggestions du Jour',
                                 '[CARTE] Methode Calcul de Prix','[CARTE] Prix Trouves Justes pour Clients','[CARTE] Prix Trouves Justes pour Soi',
                                 "[RECETTES] Support Memorisation","[RECETTES] Satisfait par ce Support?","[RECETTES] Temps Passe (min/recette)","[RECETTES] Est-ce-trop?","[RECETTES] Methode Transmission du Savoir","[RECETTES] Satisfait par ce Mode de Transmission?",
                                 "[COMMANDES] Methode Passage Commandes","[COMMANDES] Frequence Passage Commandes","[COMMANDES] Temps Passe par Jour","[COMMANDES] Temps Ideal par Jour",
                                 "[COMMANDES] Support Memorisation","[COMMANDES] Methode Classement des Commandes","[COMMANDES] Methode Classement des Bons de Livraison","[COMMANDES] Methode Classement des Factures","[COMMANDES] Methode Transmission des Factures","[COMMANDES] Proportion Factures par Mail","[COMMANDES] Nombre Fournisseurs",
                                 "[COMPTA] Moyen Obtention Coefficient","[COMPTA] Support Comptabilite","[COMPTA] Outil Utilise","[COMPTA] Frequence Connaissance Coefficient","[COMPTA] Souhait de Plus de Regularite?","[COMPTA] Depense Moyenne pour Obtention Bilan","[COMPTA] Unite","[COMPTA] Prix Consenti pour Notre Plateforme",
                                 "[PREFERENCES] Premiere Fonctionnalite Preferee","[PREFERENCES] Deuxieme Fonctionnalite Preferee","[PREFERENCES] Troisieme Fonctionnalite Preferee",
                                  "[GENERAL] Metier","[GENERAL] Age","[GENERAL] Experience","[GENERAL] Nombre Couverts","[GENERAL] Nombre Places","[GENERAL] Nombre Cuisiniers","[GENERAL] Prix Moyen Assiette","[GENERAL] Nombre Etablissements"])
    users = User.objects.all()
    for user in users:
        if not (user.is_staff or user.is_superuser or user.randomly_created):
            try:
                player = Player.objects.get(user = user)
                carte_form = CarteFormAnswer.objects.get(player=player)
                recette_form = RecetteFormAnswer.objects.get(player=player)
                commande_form = CommandeFormAnswer.objects.get(player=player)
                compta_form = ComptaFormAnswer.objects.get(player=player)
                fonctionnalites_prefereers_form = FonctionnalitesPrefereesFormAnswer.objects.get(player=player)
                general_info_form = GeneralIntroductionFormAnswer.objects.get(player=player)
                writer.writerow([user.full_name(), 
                                             player.is_validated,
                                             f"{value_or_blank_value(carte_form.frequence_modification)}", 
                                             f"{value_or_blank_value(carte_form.rythme_trouve_suffisant)}", 
                                             f"{value_or_blank_value(carte_form.frequence_suggestion_du_jour)}", 
                                             f"{value_or_blank_value(carte_form.methode_calcul_de_prix)}", 
                                             f"{value_or_blank_value(carte_form.prix_trouve_justes_clients)}", 
                                             f"{value_or_blank_value(carte_form.prix_trouve_justes_soi)}",

                                             f"{value_or_blank_value(recette_form.support_memorisation)}",  
                                             f"{value_or_blank_value(recette_form.satisfait_support_memorisation)}",
                                             f"{value_or_blank_value(recette_form.temps_passe_minute_par_recette)}",
                                             f"{value_or_blank_value(recette_form.est_ce_trop)}",
                                             f"{value_or_blank_value(recette_form.methode_transmission_savoir)}",
                                             f"{value_or_blank_value(recette_form.satisfait_mode_transmission)}",

                                             f"{value_or_blank_value(commande_form.methode_passage_commande)}",
                                             f"{value_or_blank_value(commande_form.frequence_passage_commande)}",
                                             f"{value_or_blank_value(commande_form.temps_passe_par_jour)}",
                                             f"{value_or_blank_value(commande_form.temps_ideal_par_jour)}",
                                             f"{value_or_blank_value(commande_form.support_memorisation)}",
                                             f"{value_or_blank_value(commande_form.methode_classement_commandes)}",
                                             f"{value_or_blank_value(commande_form.methode_classement_bons_livraison)}",
                                             f"{value_or_blank_value(commande_form.methode_classement_factures)}",
                                             f"{value_or_blank_value(commande_form.methode_transmission_facture)}",
                                             f"{value_or_blank_value(commande_form.proportion_factures_par_mail)}",
                                             f"{value_or_blank_value(commande_form.nombre_fournisseurs)}",

                                             f"{value_or_blank_value(compta_form.moyen_obtention_coefficients)}",
                                             f"{value_or_blank_value(compta_form.support_comptablitie)}",
                                             f"{value_or_blank_value(compta_form.outil_utilise)}",
                                             f"{value_or_blank_value(compta_form.frequence_connaissance_coefficient)}",
                                             f"{value_or_blank_value(compta_form.souhait_plus_de_regularite)}",
                                             f"{value_or_blank_value(compta_form.depense_moyenne_obtention_bilan)}",
                                             f"{value_or_blank_value(compta_form.unite_cout_optention_bilan)}",
                                             f"{value_or_blank_value(compta_form.depense_consentie_notre_version)}",

                                              f"{value_or_blank_value(fonctionnalites_prefereers_form.premiere_fonctionnalite)}",
                                              f"{value_or_blank_value(fonctionnalites_prefereers_form.deuxieme_fonctionnalite)}",
                                              f"{value_or_blank_value(fonctionnalites_prefereers_form.troisieme_fonctionnalite)}",

                                              f"{value_or_blank_value(general_info_form.metier)}",
                                              f"{value_or_blank_value(general_info_form.age)}",
                                              f"{value_or_blank_value(general_info_form.experience)}",
                                              f"{value_or_blank_value(general_info_form.nombre_couverts)}",
                                              f"{value_or_blank_value(general_info_form.nombre_places)}",
                                              f"{value_or_blank_value(general_info_form.nombre_cuisiniers)}",
                                              f"{value_or_blank_value(general_info_form.prix_moyen_assiette)}",
                                              f"{value_or_blank_value(general_info_form.nombre_etablissements)}",
                                             ])
            except Exception as e:
                print(e)
                writer.writerow([f"ERROR READING {user.full_name()}"])
    return response





def value_or_blank_value(value):
    if value:
        return value
    else:
        return "?"