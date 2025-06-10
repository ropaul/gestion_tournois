import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import gestion_formulaire_inscription
import pandas as pd
import util
import logging

def send_mail(smtp_username: str, smtp_password: str,email_receiver: list[str], objet: str, corps: str):
    # Configuration du serveur SMTP
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # Création du message
    message = MIMEMultipart()
    message['From'] = smtp_username
    message['Bcc'] = email_receiver
    message['Subject'] = objet

    # Corps du message
    body = corps
    message.attach(MIMEText(body, 'plain'))

    # Connexion au serveur SMTP et envoi de l'e-mail
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        # envoie en copie caché.
        server.sendmail(message['From'], message['Bcc'] , message.as_string())
        print('E-mail envoyé avec succès!')
    except Exception as e:
        logging.error(f'Erreur lors de l\'envoi de l\'e-mail : {e}')
        print(f'Erreur lors de l\'envoi de l\'e-mail : {e}')
    finally:
        server.quit()

def send_mail_to_participant(list_tournoi, formulaire_enrichi, configuration, text_inscription, text_attente, text_refus,credential_gmail ):
    # pour chaque etat possible, on associe le corps du mail en parametre
    dict_etat_corps= {"participant": text_inscription, "attente": text_attente, "refuser":text_refus }
    param_gmail = util.read_param(credential_gmail)
    smtp_username = param_gmail['smtp_username']
    smtp_password = param_gmail['smtp_password']
    df_configuration = pd.read_csv(configuration)
    for tournoi in formulaire_enrichi["liste_tournois"].unique().tolist():
        print(tournoi)
        formulaire_restreint = formulaire_enrichi[formulaire_enrichi["liste_tournois"] == tournoi]
        for etat, corps in dict_etat_corps.items():
            f = open(corps, 'r', encoding='utf-8')
            contenu = f.read()
            corps_enrichi = contenu.format(tournoi = tournoi, heure= df_configuration[df_configuration["libelle"] == tournoi]["heure"].to_string())
            column_etat = "etat"
            list_mail=formulaire_restreint[formulaire_restreint[column_etat] == etat]["Adresse Mail"].tolist()
            list_mail = ", ".join(list_mail)
            objet_mail = "[Paris est Ludique]" + tournoi + ": " + etat

            if etat != "participant"  and len(list_mail) != 0:
                logging.info(" pour le tournoi {tournoi}, avec l'état {etat} mail envoyé à {list} ".format(tournoi = tournoi,etat = etat, list = list_mail))
                send_mail(smtp_username, smtp_password,list_mail,objet_mail, corps_enrichi)
            f.close()


if __name__ == '__main__':
    credential_gmail,configuration_tournoi, formulaire, resultat, text_inscription, text_attente, text_refus = util.get_file()
    param_gmail = util.read_param(credential_gmail)
    smtp_username = param_gmail['smtp_username']
    smtp_password = param_gmail['smtp_password']
    list_tournoi, formulaire_enrichi = result = gestion_formulaire_inscription.get_participant("configuration_tournoi", "Formulaire sans titre (réponses) - Réponses au formulaire 1.csv")
    send_mail_to_participant(list_tournoi, formulaire_enrichi, configuration_tournoi,"text_inscription", "text_liste_attente", "text_refus", credential_gmail )

