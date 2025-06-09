import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import gestion_formulaire_inscription
import pandas as pd
import util


def send_mail(smtp_username: str, smtp_password: str,email_receiver: list[str], objet: str, corps: str):
    # Configuration du serveur SMTP
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # Création du message
    message = MIMEMultipart()
    message['From'] = smtp_username
    message['To'] = email_receiver
    message['Subject'] = objet

    # Corps du message
    body = corps
    message.attach(MIMEText(body, 'plain'))

    # Connexion au serveur SMTP et envoi de l'e-mail
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(message['From'], message['To'], message.as_string())
        print('E-mail envoyé avec succès!')
    except Exception as e:
        print(f'Erreur lors de l\'envoi de l\'e-mail : {e}')
    finally:
        server.quit()

def send_mail_to_participant(list_tournoi, formulaire_enrichi, configuration, text_inscription, text_attente, text_refus,credential_gmail ):
    # pour chaque etat possible, on associe le corps du mail en parametre
    dict_etat_corps= {"participe": text_inscription, "attente": text_attente, "refuser":text_refus }
    param_gmail = util.read_param(credential_gmail)
    smtp_username = param_gmail['smtp_username']
    smtp_password = param_gmail['smtp_password']
    df_configuration = pd.read_csv(configuration)
    print(df_configuration)
    for tournoi in list_tournoi:
        for etat, corps in dict_etat_corps.items():
            f = open(corps, 'r')
            contenu = f.read()
            corps_enrichi = contenu.format(tournoi = tournoi, heure= df_configuration[df_configuration["libelle"] == tournoi]["heure"].to_string())
            print(corps_enrichi)
            column_etat = "etat_" + str(tournoi)
            list_mail=formulaire_enrichi[formulaire_enrichi[column_etat] == etat]["adresse mail"].tolist()
            list_mail = ", ".join(list_mail)
            print (list_mail)
            objet_mail = df_configuration[df_configuration["libelle"] == tournoi]["objet"].to_string()
            send_mail(smtp_username, smtp_password,list_mail,objet_mail, corps_enrichi)
            f.close()


if __name__ == '__main__':
    credential_gmail,configuration_tournoi, formulaire, resultat, text_inscription, text_attente, text_refus = util.get_file()
    param_gmail = util.read_param(credential_gmail)
    smtp_username = param_gmail['smtp_username']
    smtp_password = param_gmail['smtp_password']
    list_tournoi, formulaire_enrichi = result = gestion_formulaire_inscription.get_participant("configuration_tournoi", "Formulaire sans titre (réponses) - Réponses au formulaire 1.csv")
    send_mail_to_participant(list_tournoi, formulaire_enrichi, configuration_tournoi,"text_inscription", "text_liste_attente", "text_refus", credential_gmail )

