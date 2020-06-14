# Renouvellement Helloassos 
Utilisations des payements pour le renouvellement 
## Match nom, prenom , date de naissance 
Afin de savoir quand a été le dernier paiement pour un membre 

# Database 

**Table of association** 

CREATE TABLE `association` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`client_id` varchar(250) NOT NULL,
`client_secret` varchar(250) NOT NULL,
`association` varchar(250) NOT NULL,
`campagne` varchar(300) NOT NULL,
`login_email` varchar(300) DEFAULT NULL,
`password_email` varchar(300) DEFAULT NULL,
`server_email` varchar(300) DEFAULT NULL,
`server_email_port` int(11) DEFAULT NULL,
`email_template` text DEFAULT NULL,
PRIMARY KEY (`id`)
);

**Table of email sent to adherant** 

CREATE TABLE `email_sent` (
  `idemail_sent` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(250) DEFAULT NULL,
  `association` varchar(250) DEFAULT NULL,
  `campagne` varchar(250) DEFAULT NULL,
  `date` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idemail_sent`)
) ;


# Librairie nécéssaire 

mysql-connector-python and requests

Il est possible d'utiliser les commandes suivantes directement dans le code pour le téléchargement automatique des librairies.

import sys

import subprocess

subprocess.check_call([sys.executable, "-m", "pip", "install", 'mysql-connector-python'])

subprocess.check_call([sys.executable, "-m", "pip", "install", 'requests'])

# Token helloassos

helloassos.com => mon compte => intégration/API

# Configuration db

Fichier de configuration.ini a rajouté au projet

[DB]

host=X

user=X

password=X

database=X
