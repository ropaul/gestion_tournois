# gestion_tournois

Ce script est fait pour gérer plus facilement les inscriptions aux tournois. Il est utilisé pour un festival de jeux de société.
Pour qu'il fonctionne, il lui faut plusieurs fichier dont le formulaire googleForm créé pour les tournois.

il fait 2 choses :
- création d'un fichier afin de savoir qui participe, qui est sur liste d'attente et qui est refusé
- envoi des mails aux personnes sur liste d'attente et aux personnes refusées.

Afin de savoir ce qu'il s'est passé dans le script, le fichier log.txt enregistre tous les mails envoyés, ainsi que les eventuelles erreurs que le scipt peut rencontrer.

Pour qu'il fonctionne vous devez:
- ajouter le formulaire dans le même dossier que l'executable.
- si vous avez déjà utiliser le scipt, vous devez enlever les lignes déjà traité auparavant (vous pouvez regarder le fichier out.csv)
- changer la configuration des tournois pour prendre en compte le nombre de personnes déjà inscrite. En fait vous avez a faire les 2 dernieres étapes que pour les tournois dont le nombre de participant est déjà atteint.
- lancer le script_tournois.exe

Ce script est hautement (trop) paramétrable. Plusieurs fichiers sont nécéssaires :

##file_name
fichier de configuration pour les différents autres fichiers. Il est le seul fichier qui DOIT s'appeler tel que décrit ici. Plusieurs variables doivent être remplies:
- credential_gmail=credential_gmail
- configuration_tournoi=configuration_tournoi
- formulaire=[test] Copie de Inscription Tournoi PEL 2025 pour des tests .csv
- resultat=resume.csv
- text_inscription=text_inscription
- text_attente=text_liste_attente
- text_refus=text_inscription

les points ci-dessus sont les variables à remplir, ici avec un exemple.

##credential_gmail
fichier afin d'avoir les credentials pour le compte mail qui va envoyer les mails.
Il faut un mot de passe applicatif. Si vous cherchez sur gmail, l'option n'est pas disponible tant que vous n'avez pas activer l'authentification à 2 facteurs.


##configuration_tournoi
un fichier .csv avec pour chaque tournoi, les champs suivant:
- libelle
- heure
- nombre_participant
- nombre_attente
voici un exemple : 
samedi 11h - Heat ,05/07/2025,25,100

oui, l'heure est une date et elle n'est pas utilsée dans le script. Je viens de m'en apercevoir mais je n'enlèverai pas ce champs. Vous pouvez le faire, mais il y a une chance non nul que le script ne marche plus par la suite.

## formulaire
LE fichier le plus important car c'est celui qui traitera le formulaire du google form.
Normalement, vous qui lisez ces lignes, vous avez accès à ce formulaire. Dans le cas contraire, veuillez contacter les personnes compétentes.

##resultat
c'est normalement le nom du fichier de sortie. A l'heure où j'écris ces mots, ce paramètre n'est pas pris en compte et le fichier de sortie s'appelle out.csv.
Si cela est inaceptable, veuillez me contacter.

##text_inscription
le corps du mail à envoyer lors d'une inscription. Pour l'instant pas utilisé car seul ceux sur liste d'attente et ceux refusés recevront des mails.

##text_attente
le seul corps de mail avec vraiment de l'intéret au vu de la configuration. Est envoyé à toutes les personnes sur liste d'attente. Le {tournoi} fait référence au nom du tournoi dans le formulaire.

##text_refus
corps de mail pour les refus.

#le fichier .exe
Ce .exe à été créer avec pyinstaller

(https://github.com/ropaul/gestion_tournois)


