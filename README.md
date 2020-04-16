# CDN minimliste de Geotribu

Fichiers de configuration pour <https://cdn.geotribu.fr>.

## Déploiement

> OS serveur : Ubuntu Server 18.04

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
