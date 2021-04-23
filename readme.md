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
* Tapez : python -m venv env
* Tapez :
    * Pour Windows : env\Scripts\activate.bat
    * Pour Linux   : env/bin/activate
    
* Tapez : pip install -r requirements.txt
* Tapez : python app.py

## Rapport flake8-html

* Ouvrez un invite de commande
* Placez vous dans le dossier contenant le fichier app.py
* Tapez : flake8 --format=html --htmldir=flake-report --max-line-length=119 model.py view.py controller.py app.py