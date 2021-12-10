## BENABDALLAH_Twitter_Sentiments


# API :


# Instalation :

- D'abbord il faut créé notre environement Python avec :

```shell
python3 -m venv env
```

- Activer l'environement : 

```shell
source env/bin/activate
```

- Installer les dépendances et les librairie nécessaire pour ce projet présente dans le fichier `requirements.txt` :

```shell
pip install -r requirements.txt
```


# Lancement du Serveur en local:

- Pour démarrer notre serveur Flask :

```shell
export FLASK_APP=app
export FLASK_ENV=development
flask run
```

Le serveur démarre à l'adresse : `http://127.0.0.1:5000/`