# Interface de gestion des fichiers du CDN

L'outil utilisé est [Tiny File Manager](https://tinyfilemanager.github.io/).

> Voir [l'article présentant le fonctionnement sur Geotribu](https://static.geotribu.fr/contribuer/guides/image/#parcourir-les-images-sur-le-cdn-de-geotribu).

## Installation

1. Installer les dépendances

    ```bash
    # mise à jour de la liste des paquets
    sudo apt update
    # ajout du PPA pour avoir les dernières versions
    sudo apt install software-properties-common
    sudo add-apt-repository ppa:ondrej/php

    # installation de PHP et de ses dépendances
    sudo apt install php7.4 php7.4-zip php7.4-mbstring php7.4-fileinfo php7.4-iconv libapache2-mod-php
    ```

2. Télécharger et installer [Tiny File Manager](https://tinyfilemanager.github.io/) dans `/var/www/geotribu/cdn/`.
3. Se baser sur le fichier [./tinyfilemanager.php] de ce dépôt pour la configuration et faire les adaptations nécessaires.
4. Copier les images dans `/var/www/geotribu/cdn/images`.
5. Définir les droits :

    ```bash
    sudo chown -R geotribu:www-data /var/www/geotribu/cdn/
    sudo chmod -R 770 /var/www/geotribu/cdn/
    ```

:warning: La base de données des commentaires étant stockée dans l'arborescence, il s'agit de s'assurer que les droits sont bien adaptés. Voir : <https://github.com/geotribu/comments>.

### Configuration Apache

#### Ajouter les mime-types manquants

```sh
sudo nano /etc/mime.types
```

Ajouter `image/webp             webp` à la suite des formats d'images.

----

### Aperçu de l'arborescence

![Arborescence des scripts sur le serveur](docs/_static/img/scripts_arborescence.png "Organisation des fichiers sur le serveur")

----

## Ressources

- Apache 2.x
- [Tiny File Manager](https://tinyfilemanager.github.io/)
