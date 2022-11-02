# CDN minimaliste de Geotribu

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/geotribu/minimalist-cdn/master.svg)](https://results.pre-commit.ci/latest/github/geotribu/minimalist-cdn/master)

Fichiers de configuration pour <https://cdn.geotribu.fr> et des outils liés : sauvegarde, notifications, indexation...

## Déploiement

- OS serveur à date : Ubuntu Server 22.04

### Prérequis

- Accès SSH au serveur. Exemple de configuration SSH :

    ```config
    IdentitiesOnly yes

    Host geotribu
        HostName vps383.altinea.eu
        User geotribu
        IdentityFile ~/.ssh/id_rsa_elgeopaso
    ```

- Ansible : voir [le README dédié](ansible/README.md)
- Mot de passe maître pour les variables secrètes d'Ansible (voir le même README)

----

## Outils liés

### Interface minimaliste de gestion des fichiers

Voir [le README dédié](cdn/README.md).

### Sauvegarde

Voir [le README dédié](ansible/roles/backup/README.md).

### Notifications

Voir [le README dédié](notifications/README.md).

### Indexation des fichiers du CDN

Afin de faciliter la recherche de la bonne image lors de la rédaction des contenus, un index des fichiers du CDN est réalisé avec [lunr](https://lunrjs.com/) (son implémentation Python).

Voir [le README dédié](search-index/README.md).
