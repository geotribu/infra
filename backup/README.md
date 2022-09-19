# Sauvegarde du CDN

> Voir [l'article présentant le fonctionnement sur Geotribu](https://static.geotribu.fr/contribuer/internal/backup/).

## GitHub CLI

L'outil en ligne de commande de GitHub est utilisé pour créer des releases et téléverser les sauvegardes des fichiers statiques.

1. Installer GitHUB CLI : <https://github.com/cli/cli/blob/trunk/docs/install_linux.md#debian-ubuntu-linux-raspberry-pi-os-apt>
2. Cloner le dépôt du site :

```bash
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
