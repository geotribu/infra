# CDN minimaliste de Geotribu

Fichiers de configuration pour <https://cdn.geotribu.fr> et du mécanisme de sauvegarde, basé sur GitHub Release.

## Déploiement

> OS serveur : Ubuntu Server 18.04

### Tiny File Manager

```bash
# mise à jour de la liste des paquets
sudo apt update
# ajout du PPA pour avoir les dernières versions
sudo apt install software-properties-common
sudo add-apt-repository ppa:ondrej/php

# installation de PHP et de ses dépendances
sudo apt install php7.4 php7.4-zip php7.4-mbstring php7.4-fileinfo php7.4-iconv libapache2-mod-php
```

Installer [Tiny File Manager](https://tinyfilemanager.github.io/) dans `/var/www/geotribu/cdn/`.

Se baser sur le fichier [./tinyfilemanager.php] de ce dépôt pour la configuration et faire les adaptations nécessaires.

Copier les images dans `/var/www/geotribu/cdn/images`.

Définir les droits :

```bash
sudo chown -R geotribu:www-data /var/www/geotribu/cdn/
sudo chmod 770 /var/www/geotribu/cdn/
```

### GitHub CLI

L'outil en ligne de commande de GitHub est utilisé pour créer des releases et téléverser les sauvegardes des fichiers statiques.

```bash
# dépendances
sudo apt install dirmngr

# ajout de la clé et du dépôt
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key C99B11DEB97541F0
sudo apt-add-repository https://cli.github.com/packages

# installation
sudo apt update
sudo apt install gh

# clonage du dépôt du site
cd /var/www/geotribu/
git clone https://github.com/geotribu/website.git --depth=1
```

Pour finir, s'authentifier à GitHub via un Personal Token - Suivre la [documentation](https://cli.github.com/manual/).

### Script de sauvegarde

1. Copier le fichier `backup.sh` :

    ```bash
    scp backup.sh geotribu@elgeopaso.georezo.net:/home/geotribu/scripts/geotribu-backup/
    ```

2. Activer la planification via un cron

    ```bash
    crontab -e
    ```

    ```cron
    @monthly /home/geotribu/scripts/geotribu-backup/backup.sh
    ```

----

## Ressources

- Apache 2.x
- [Tiny File Manager](https://tinyfilemanager.github.io/)
- [GitHub CLI](https://cli.github.com/)
