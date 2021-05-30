# Description du programme
Ce programme permet la gestion de tournoi d'échec.  

Pour une utilisation rapide :  
* Commencez par importer au moins 8 joueurs en base de données.
* Créer un tournoi
* Importer 8 joueurs dans le tournoi
* Créer un round
* Clôturer le round
* Réitérer les deux derniers points jusqu'a la fin du tournoi

Attention : N'oubliez pas d'exporter le tournoi à tout moment pour sauvegarder sont contenue

## Lancement du programme

* Ouvrez un invite de commande
* Placez vous dans le dossier contenant le fichier app.py
* Création de l'environnement virtuel : ```python -m venv env```
* Activation de l'environnement virtuel :
    * Pour Windows : ```env\Scripts\activate.bat```
    * Pour Linux   : ```env/bin/activate```
* Installation des dépendances : ```pip install -r requirements.txt```
* Lancement du programme : ```python app.py```

## Rapport flake8-html

* Ouvrez un invite de commande
* Placez vous dans le dossier contenant le fichier app.py
* Création du rapport : ```flake8 model.py view.py controller.py app.py```