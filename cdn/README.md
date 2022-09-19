# Interface de gestion des fichiers du CDN

L'outil utilisé est [Tiny File Manager](https://tinyfilemanager.github.io/).

> Voir [l'article présentant le fonctionnement sur Geotribu](https://static.geotribu.fr/contribuer/guides/image/#parcourir-les-images-sur-le-cdn-de-geotribu).

## Installation

1. Installer les dépendances

    ```bash
    # mise à jour de la liste des paquets
    sudo apt update
    # ajout du PPA pour avoir les dernières versions de PHP et d'Apache
    sudo apt install software-properties-common
    sudo add-apt-repository ppa:ondrej/php
    sudo add-apt-repository ppa:ondrej/apache2

    # installation de PHP et de ses dépendances
    sudo apt install php8.1 php8.1-common php8.1-fileinfo php8.1-fpm php8.1-iconv php8.1-mbstring php8.1-zip
    ```

1. Configurer Apache :

    ```bash
    # activation des modules (compression et http2)
    sudo a2enmod brotli
    sudo a2enmod http2
    sudo a2enmod proxy_fcgi setenvif
    sudo a2enmod mpm_event
    sudo a2dismod mpm_prefork

    # activation des configurations complémentaires
    sudo a2enconf php8.1-fpm
    ```

1. Télécharger et installer [Tiny File Manager](https://tinyfilemanager.github.io/) dans `/var/www/geotribu/cdn/`.
1. Se baser sur le fichier [./tinyfilemanager.php] de ce dépôt pour la configuration et faire les adaptations nécessaires.
1. Copier les images dans `/var/www/geotribu/cdn/images`.
1. Définir les droits :

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

#### HTTP/2

Tester :

```bash
> curl -I --http2 -s https://cdn.geotribu.fr/ | grep HTTP
HTTP/2 200
```

Ressources :

- documentation Apache : <https://httpd.apache.org/docs/2.4/howto/http2.html>
- manipulation à faire pour utiliser la version 2 du protocole : <https://serverfault.com/questions/888453/getting-http-2-working-on-apache-2-4-29-on-debian-8>.

----

### Aperçu de l'arborescence

![Arborescence des scripts sur le serveur](docs/_static/img/scripts_arborescence.png "Organisation des fichiers sur le serveur")

----

## Ressources

- Apache 2.x
- [Tiny File Manager](https://tinyfilemanager.github.io/)
