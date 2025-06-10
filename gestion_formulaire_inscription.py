from datetime import datetime

import pandas as pd
from functools import reduce
import logging

def read_parameter(name):
    parameter_tournoi = pd.read_csv(name)
    return parameter_tournoi

def read_formulaire(name):
    formualire = pd.read_csv(name)
    return formualire

# fonction pour recuperer la liste des pariticpant et des personnes en liste d'atente en fonction des parametre des tournoir
# il faut rajouter la gestion des mails déja envoyé
def get_participant_with_files(nom_tounoi, parametre, formulaire):
    etat_torunoi= []

    nb_participant= int(parametre[parametre["libelle"] == nom_tounoi]["nombre_participant"].iloc[0])
    nb_attente = int(parametre[parametre["libelle"] == nom_tounoi]["nombre_attente"].iloc[0])
    formulaire_tournoi = formulaire[formulaire[nom_tounoi]== "oui"]

    # on calcul le nombre de participant
    min_nb_participant = min(nb_participant, len(formulaire_tournoi) )
    for n in range(min_nb_participant):
        etat_torunoi.append("participe")
    #  si il reste du monde, on les mets dans une liste d'attente
    if (min_nb_participant != len(formulaire_tournoi) ):
        min_nb_attente = min(nb_attente, len(formulaire_tournoi) )
        for n in range(min_nb_attente):
            etat_torunoi.append("attente")
        #  si il y a encore trop de monde, on les mets en refus
        if (min_nb_attente != len(formulaire_tournoi) ):
            min_nb_refuser =  len(formulaire_tournoi)
            for n in range(min_nb_refuser):
                etat_torunoi.append("refuser")
    name_column = "etat_" + str(nom_tounoi)
    formulaire_tournoi = formulaire_tournoi.assign(name_column = etat_torunoi)
    formulaire_tournoi = formulaire_tournoi.rename(columns={"name_column": name_column})
    return formulaire_tournoi

def get_participant_with_files2(nom_tounoi, parametre, formulaire):

    nb_participant= int(parametre[parametre["libelle"] == nom_tounoi]["nombre_participant"].iloc[0])
    nb_attente = int(parametre[parametre["libelle"] == nom_tounoi]["nombre_attente"].iloc[0])
    formulaire_tournoi = formulaire[formulaire["liste_tournois"].str.contains(nom_tounoi, case=False, na=False)]

    etat_torunoi= ["participant"] * min(len(formulaire_tournoi), nb_participant) \
                    + ["attente"] * min(len(formulaire_tournoi) - nb_participant, nb_attente)\
                    + ["refuser"] * max(0, len(formulaire_tournoi) - nb_participant - nb_attente)
    name_column = "etat"
    formulaire_tournoi = formulaire_tournoi.assign(name_column = etat_torunoi)
    formulaire_tournoi = formulaire_tournoi.rename(columns={"name_column": name_column})
    return formulaire_tournoi


def get_participant( name_parameter, name_formulaire):
    parameter_tounoi = read_parameter(name_parameter)
    formulaire = read_formulaire(name_formulaire)


    formulaire = formulaire.rename(columns={"A quel tournoi souhaitez-vous vous inscrire?": "samedi","A quel tournoi souhaitez-vous vous inscrire?.1": "dimanche"})
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    formulaire['samedi'] = formulaire['samedi'].apply(lambda x: "samedi " + x)
    formulaire['dimanche'] = formulaire['dimanche'].apply(lambda x: "dimanche " + x)


    # Utiliser melt pour fusionner colonne1 et colonne2
    formulaire = formulaire.melt(
        id_vars=["Horodateur","Nom ou Pseudo","Adresse Mail","Numéro de téléphone"],  # Colonnes à conserver telles quelles
        value_vars=['samedi', 'dimanche'],  # Colonnes à fusionner
        value_name='liste_tournois',  # Nom de la nouvelle colonne fusionnée
        var_name='origine')  # Optionnel : nom de la colonne indiquant l'origine

    list_column = list(formulaire.columns.values)
    list_tournoi = parameter_tounoi["libelle"].to_list()
    tournois = []
    for l in list_tournoi :
        tournois.append(get_participant_with_files2(l, parameter_tounoi, formulaire))


    df = reduce(lambda df1,df2: pd.concat([df1, df2], ignore_index=True), tournois)
    logging.info("creation du fichier out.csv avec résumé de ce qui se passe")
    df.to_csv('out' + str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) + '.csv', index=False)
    print(df)

    return list_tournoi, df


if __name__ == '__main__':
    # parameter_tounoi = read_parameter("configuration_tournoi")
    # # print(parameter_tounoi)
    # formulaire = read_formulaire("Formulaire sans titre (réponses) - Réponses au formulaire 1.csv")
    # # print(formulaire)
    # participant = get_participant_with_files("tournoi 1 leaders", parameter_tounoi, formulaire)
    # print(participant )
    # participant = get_participant_with_files("tournoi 2 harmonies", parameter_tounoi, formulaire)
    # print(participant )
    # participant = get_participant_with_files("tournoi 3 garden rush", parameter_tounoi, formulaire)
    # print(participant )

    # test final
    list_tournoi, result = get_participant("configuration_tournoi", "[test] Copie de Inscription Tournoi PEL 2025 pour des tests .csv")

    print(result)