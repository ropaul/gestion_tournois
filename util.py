


def read_param(name_file):
    # Chemin vers le fichier texte
    file_path = name_file

    # Dictionnaire pour stocker les paramètres
    params = {}

    # Lire le fichier texte
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Supprimer les espaces et les sauts de ligne
            line = line.strip()
            # Ignorer les lignes vides et les commentaires
            if line and not line.startswith('#'):
                # Diviser la ligne en clé et valeur
                key, value = line.split('=', 1)
                params[key.strip()] = value.strip()

    return params

def get_file():
    params = read_param("file_name")
    credential_gmail = params['credential_gmail']
    configuration_tournoi = params['configuration_tournoi']
    formulaire = params['formulaire']
    resultat = params['resultat']
    text_inscription=params['text_inscription']
    text_attente=params['text_attente']
    text_refus=params['text_inscription']
    return credential_gmail,configuration_tournoi, formulaire, resultat, text_inscription, text_attente, text_refus
