# Création d'un index de recherche pour les fichiers du CDN

## Prérequis

- Python 3.7+
- [lunr.py](https://lunr.readthedocs.io/)
- accès SSH au serveur cible (voir configuration sur le [README du dépôt](../README.md))

## Installation

Depuis ce dossier :

```bash
# création du dossier où stocker le script
ssh geotribu mkdir -p ~/scripts/cdn-search-index/
# copie du script, de la configuration et du fichier de dépendances sur le serveur
scp images-indexer.ini requirements.txt search_indexer.py geotribu:~/scripts/cdn-search-index/
```

Créer un environnement virtuel dans le même dossier :

```bash
ssh geotribu

# créer l'environnement virtuel
cd ~/scripts/cdn-search-index/
python3 -m venv .venv

# l'activer
source .venv/bin/activate

# installer les dépendances
python -m pip install -U pip
python -m pip install -U setuptools wheel
python -m pip install -U -r requirements.txt
```

## Configuration

Eventuellement, modifier le fichier `images-indexer.ini` pour configurer les paramètres de l'indexation :

```bash
nano images-indexer.ini
```

## Utilisation

### Indexation

Le script `search_indexer.py` génère le fichier d'index.

Tester l'indexation depuis le serveur :

```bash
# activer l'environnement virtuel
cd ~/scripts/cdn-search-index/
source .venv/bin/activate

# indexer les images
python -d search_indexer.py
```

Le fichier d'index est ensuite accessible publiquement : <https://cdn.geotribu.fr/img/search-index.json>.

### Recherche

Le script `search_playground.py` permet de faire une recherche en utilisant l'index.
