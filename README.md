# Infra Geotribu

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/geotribu/infra/master.svg)](https://results.pre-commit.ci/latest/github/geotribu/infra/master) [![ansible-lint Linter](https://github.com/geotribu/infra/actions/workflows/ansible-linter.yml/badge.svg)](https://github.com/geotribu/infra/actions/workflows/ansible-linter.yml)

Fichiers de configuration et de déploiement des différents composants constituant l'infra du projet [Geotribu](https://geotribu.fr/) :

- principalement le site d'hébergement des fichiers statiques (images...) <https://cdn.geotribu.fr>
- scripts de sauvegarde
- commentaires (<https://comments.geotribu.fr/admin/>)
- notifications
- indexation des contenus

## Déploiement

- le serveur est gracieusement prêté par GeoRezo et hébergé chez [Ataraxie](https://www.ataraxie.fr/) depuis l'été 2025.
- OS serveur à date (Ataraxie) : Ubuntu Server 24.04

### Prérequis

- Accès SSH au serveur.
    1. Générer une clé dédiée :

        ```sh
        ssh-keygen -t ed25519 -C "Geotribu prenom.nom@mail.com" -f ~/.ssh/id_ed25519_geotribu
        ```

    1. Entrer un mot de passe fort pour la clé (passphrase).
    1. Mettre sa clé publique sur le serveur (requiert l'accès par mot de passe au moins une fois) :

        ```sh
        ssh-copy-id -o PubkeyAuthentication=no -o PreferredAuthentications=password -i ~/.ssh/id_ed25519_geotribu.pub 91.230.235.162
        ```

    1. Exemple de configuration SSH :

        ```config
        IdentitiesOnly yes

        Host geotribu
            ForwardAgent yes
            HostName 91.230.235.162
            IdentityFile ~/.ssh/id_ed25519_geotribu
            Preferredauthentications publickey
            User geotribu
        ```

    1. Valider la connexion :

        ```sh
        ssh geotribu
        ```

- Ansible : voir [le README dédié](ansible/README.md)
- Mot de passe maître pour les variables secrètes d'Ansible (voir le même README)

----

## Outils liés

### Interface minimaliste de gestion des fichiers

Voir [le README dédié](ansible/roles/cdn.geotribu.fr/README.md).

### Sauvegarde

Voir [le README dédié](ansible/roles/backup/README.md).

### Indexation des fichiers du CDN

Afin de faciliter la recherche de la bonne image lors de la rédaction des contenus, un index des fichiers du CDN est réalisé avec [lunr](https://lunrjs.com/) (son implémentation Python).

Voir [le script](ansible/roles/cdn-indexer/files/search_indexer.py).

### Commentaires

Voir [le README dédié](ansible/roles/comments.geotribu.fr/README.md).
