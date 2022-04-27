# Sauvegarde du CDN

> Voir [l'article présentant le fonctionnement sur Geotribu](https://static.geotribu.fr/contribuer/internal/backup/).

## GitHub CLI

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

## Installer le script

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
