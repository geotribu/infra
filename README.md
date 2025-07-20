# Infra Geotribu

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/geotribu/infra/master.svg)](https://results.pre-commit.ci/latest/github/geotribu/infra/master)

Fichiers de configuration et de déploiement des différents composants constituant l'infra du projet [Geotribu](https://geotribu.fr/) :

- principalement le site d'hébergement des fichiers statiques (images...) <https://cdn.geotribu.fr>
- scripts de sauvegarde
- commentaires
- notifications
- indexation des contenus

## Déploiement

- le serveur est gracieusement prêté par GeoRezo et hébergé chez [Altinea](https://altinea.fr/) jusqu'à l'été 2025 puis chez [Ataraxie](https://www.ataraxie.fr/)
- OS serveur à date : Ubuntu Server 22.04

### Prérequis

- Accès SSH au serveur. Exemple de configuration SSH :

    ```config
    IdentitiesOnly yes

    Host geotribu
        HostName vps383.altinea.eu
        IdentityFile ~/.ssh/id_rsa_elgeopaso
        User geotribu
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

Voir [le script](ansible/roles/cdn-indexer/files/search_indexer.py).
