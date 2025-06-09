# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import gestion_formulaire_inscription
import mail_sender
import util
import logging

if __name__ == '__main__':

    # Configurer le système de logging pour écrire dans un fichier
    logging.basicConfig(
        filename='log.txt',  # Nom du fichier de log
        level=logging.INFO,  # Niveau de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format='%(asctime)s - %(levelname)s - %(message)s'  # Format des messages de log
    )
    # lire le fichier de parametre pour avoir les noms des différents fichiers
    print("Bonjour le PEL. On va envoyer des mails.")
    try:

        credential_gmail, configuration_tournoi, formulaire, resultat, text_inscription, text_attente, text_refus = util.get_file()
        list_tournoi, formulaire_enrichi = gestion_formulaire_inscription.get_participant(configuration_tournoi,
                                                                                          formulaire)
        mail_sender.send_mail_to_participant(list_tournoi, formulaire_enrichi, configuration_tournoi, text_inscription,
                                             text_attente, text_refus, credential_gmail)
    except Exception as e:
        # Capturer l'exception et l'écrire dans le fichier de log
        logging.error("Une erreur est survenue : %s", str(e), exc_info=True)
        raise e
    print("mails envoyé <3")