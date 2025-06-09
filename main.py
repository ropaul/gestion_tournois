# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import gestion_formulaire_inscription
import mail_sender
import util

if __name__ == '__main__':
    # lire le fichier de parametre pour avoir les noms des différents fichiers
    print("Bonjour le PEL. On va envoyer des mails.")
    credential_gmail,configuration_tournoi, formulaire, resultat, text_inscription, text_attente, text_refus = util.get_file()
    # print(credential_gmail,configuration_tournoi, formulaire, resultat )
    # param_gmail = read_param(credential_gmail)
    # smtp_username = param_gmail['smtp_username']
    # smtp_password = param_gmail['smtp_password']
    list_tournoi, formulaire_enrichi = gestion_formulaire_inscription.get_participant(configuration_tournoi, formulaire)
    mail_sender.send_mail_to_participant(list_tournoi, formulaire_enrichi, configuration_tournoi,text_inscription, text_attente, text_refus, credential_gmail )

# email_receiver = 'test.parisestamusant@gmail.com'
    # send_mail(smtp_username, smtp_password,  email_receiver)
    print("mails envoyé <3")