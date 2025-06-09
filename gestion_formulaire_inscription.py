import pandas as pd
from functools import reduce

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

def get_participant( name_parameter, name_formulaire):
    parameter_tounoi = read_parameter(name_parameter)
    formulaire = read_formulaire(name_formulaire)
    list_column =  list(formulaire.columns.values)

    list_tournoi = parameter_tounoi["libelle"].to_list()
    tournois = []
    for l in list_tournoi :
        tournois.append(get_participant_with_files(l, parameter_tounoi, formulaire))

    # print(participants)
    # on merge tous les dataframes tournois ensemble. Mais on peut ptet faire autrement
    df = reduce(lambda df1,df2: pd.merge(df1,df2,on=list_column, how="outer"), tournois)
    # df = pd.merge( tournois,  on=['nom',"prénom","adresse mail"], how="outer")
    df.to_csv('out.csv', index=False)
    return list_tournoi, df
    # dfs = [df.set_index(['nom']) for df in tournois]
    # print (pd.concat(dfs, axis=1))
    # return dfs
    # pd.DataFrame({"tournoi":list_tournoi, "participant":participants, "attente": attentes, "refusers": refusers})


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
    list_tournoi, result = get_participant("configuration_tournoi", "Formulaire sans titre (réponses) - Réponses au formulaire 1.csv")

    print(result)