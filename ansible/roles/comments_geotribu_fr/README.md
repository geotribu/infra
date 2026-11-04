# Module de commentaires pour Geotribu

Scripts et fichiers de configuration du module de commentaires du site de Geotribu, basé sur [isso](https://posativ.org/isso/) ([dépôt GitHub](https://github.com/posativ/isso)).

## Liens utiles

- URL de base de l'API de commentaires : <https://comments.geotribu.fr/>
- Interface d'administration : <https://comments.geotribu.fr/admin>
- voir aussi le [ticket sur la configuration dans MkDocs](https://github.com/squidfunk/mkdocs-material/issues/1466#issuecomment-810391442)

----

## Développement en local

1. Cloner le dépôt
2. Créer un environnement virtuel et l'activer :

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. Y installer les dépendances :

    ```bash
    python -m pip install -U pip setuptools wheel
    python -m pip install -U -r files/requirements.txt
    ```

4. Lancer l'exécution en local :

    ```bash
    isso -c isso-dev.cfg run
    ```

L'outil est accessible sur <http://localhost:8500/>.

Pour l'activer en local dans le site de Geotribu :

1. Lancer le site en local (voir [le guide dédié](https://geotribu.fr/contribuer/edit/local_edition_setup/))
2. Adapter l'URL dans [la configuration de MkDocs](https://github.com/geotribu/website/blob/master/mkdocs.yml#L111) du site. Par exemple : `comments_url=http://localhost:8500`

----

## Configuration au niveau de Gandi

### Sous-domaine

Créer un enregistrement DNS de type `A` :

```txt
comments 600 IN A 185.123.84.13
```

> Lien vers l'[interface de gestion](https://admin.gandi.net/domain/5e42db82-6b7c-11ea-8925-00163ea99cff/geotribu.fr/records)

### Compte email

Pour pouvoir envoyer des notifications, on utilise un compte email lié au domaine : <facteur@geotribu.fr>.

> Lien vers l'[interface de gestion](https://admin.gandi.net/domain/5e42db82-6b7c-11ea-8925-00163ea99cff/geotribu.fr/mail/mailboxes/5a52d348-6cbf-42f9-ab0f-7f9f21c9a8c0/edit)

### Notification Slack

Pour chaque nouveau commentaire, une notification enrichie est envoyée sur le Slack de Geotribu, via l'application Geotribot (utilisée également par le processus de sauvegarde) :

- Administration de Geotribot : <https://geotribu.slack.com/apps/A020C9Q93BK-geotribot>
- Gestion des webhooks <https://api.slack.com/apps/A020C9Q93BK>
- [Interface de conception de la notification enrichie](https://app.slack.com/block-kit-builder/TUKTSG55K#%7B%22blocks%22:%5B%7B%22type%22:%22header%22,%22text%22:%7B%22type%22:%22plain_text%22,%22text%22:%22:speech_balloon:%20Nouveau%20commentaire%22,%22emoji%22:true%7D%7D,%7B%22type%22:%22section%22,%22text%22:%7B%22type%22:%22mrkdwn%22,%22text%22:%22*Auteur(e)%20:*%20$AUTHOR_NAME%20$AUTHOR_EMAIL%20$AUTHOR_WEBSITE%22%7D%7D,%7B%22type%22:%22section%22,%22text%22:%7B%22type%22:%22mrkdwn%22,%22text%22:%22*IP%20:*%20$COMMENT_IP_ADDRESS%22%7D%7D,%7B%22type%22:%22section%22,%22text%22:%7B%22type%22:%22mrkdwn%22,%22text%22:%22*Commentaire%20:*%5Cn$COMMENT_TEXT%22%7D%7D,%7B%22type%22:%22divider%22%7D,%7B%22type%22:%22actions%22,%22elements%22:%5B%7B%22type%22:%22button%22,%22text%22:%7B%22type%22:%22plain_text%22,%22emoji%22:true,%22text%22:%22:eye-in-speech-bubble:%20Afficher%22%7D,%22url%22:%22https://geotribu.fr/rdp/2021/rdp_2021-05-07/#isso-58%22%7D,%7B%22type%22:%22button%22,%22text%22:%7B%22type%22:%22plain_text%22,%22emoji%22:true,%22text%22:%22:white_check_mark:%20Approuver%22%7D,%22style%22:%22primary%22,%22url%22:%22https://comments.geotribu.fr/id/XXXX/activate/%22%7D,%7B%22type%22:%22button%22,%22text%22:%7B%22type%22:%22plain_text%22,%22emoji%22:true,%22text%22:%22:wastebasket:%20Rejeter%22%7D,%22style%22:%22danger%22,%22url%22:%22https://comments.geotribu.fr/id/XXXX/delete/%22%7D%5D%7D%5D%7D)

:warning: Attention, cette fonctionnalité a été développée par [Julien](https://github.com/guts) et sa disponibilité dans Isso dépend de l'acceptation de la [Pull Request](https://github.com/posativ/isso/pull/724) et de la diffusion d'une nouvelle version. Si besoin, installer Isso depuis [la branche du fork](https://github.com/Guts/isso/tree/notify/webhook).

----

## Déploiement

Le module est déployé sur le serveur prêté par GeoRezo, aux côtés du [mini-CDN de Geotribu](https://github.com/geotribu/minimalist-cdn) et d'[El Geo Paso](https://github.com/Guts/elgeopaso) via Ansible.

Certaines dépendances système sont donc déjà en place sur ce serveur. Dans le cas d'une nouvelle installation, s'assurer que Python 3.10+ et SQLite sont installés.

Exemple pour Python 3.10 sur Ubuntu 22.04 :

```bash
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install build-essential python3-pip python3.7 python3.7-dev python3.7-venv sqlite3
```

### Installation

Etapes suivies, dans le cas d'un environnement Apache et mod_wsgi déjà configuré pour les besoins d'El Geo Paso (voir [la documentation](https://elgeopaso.readthedocs.io/fr/latest/deployment/apache.html)) :

```bash
cd /var/www/geotribu
mkdir comments
cd comments/
python3.7 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -U isso gevent
```

Appliquer les droits :

```bash
sudo chown -R geotribu:www-data /var/www/geotribu/cdn/
sudo chmod 770 /var/www/geotribu/cdn/
```

### Configuration Isso

Copier les fichiers `isso-prod.cfg` et `isso_wsgi.py` sur le serveur dans `/var/www/geotribu/comments`.

#### Sécurité des secrets

Paramètres à ne jamais stocker dans le dépôt ou diffuser :

- `[admin]` : `password` : mot de passe d'accès à l'interface d'administration
- `[hash]` : `salt` : chaîne de caractères aléatoire (générée avec le [module secrets de Python](https://docs.python.org/3/library/secrets.html)) utilisée pour renforcer les identifiants face aux grilles du type [Rainbow Tables](https://fr.wikipedia.org/wiki/Rainbow_table)
- `[smtp]` : `password` : mot de passe du compte email

### Configuration Apache

1. Copier et renommer le fichier `apache.vhost` en `geotribu-comments.conf` dans les sites disponibles (`/etc/apache2/sites-available`)
2. Activer le site

### Certificat SSL

1. Installer le [certbot](https://certbot.eff.org/instructions) : suivre [la documentation El Geo Paso](https://elgeopaso.readthedocs.io/fr/latest/deployment/apache.html#generer-le-certificat-ssl-avec-let-s-encrypt)
2. Lancer le processus de création des certificats :

    ```bash
    # lancer le processus en choisissant comments.
    sudo certbot --apache
    ```

    ![Certbot GeoRezo Geotribu](https://cdn.geotribu.fr/img/internal/comments/georezo_installed_sites_certbot.png "Sites identifiées par le certbot")

3. Lister les sites activés et constater que le certbot a bien fait son travail :

    ```bash
    geotribu@geotribu:~$ ls /etc/apache2/sites-enabled/
    elgeopaso.conf  elgeopaso-redirect.conf  geotribu-cdn.conf  geotribu-cdn-le-ssl.conf  geotribu-cdn-le-ssl.conf.save  geotribu-comments.conf  geotribu-comments-le-ssl.conf
    ```

### Vérifications

Vérifier que la compression est bien activée :

- sur le CSS: <https://www.whatsmyip.org/http-compression-test/?url=aHR0cHM6Ly9jb21tZW50cy5nZW90cmlidS5mci9jc3MvaXNzby5jc3M=>
- sur le JavaScript : <https://www.whatsmyip.org/http-compression-test/?url=aHR0cHM6Ly9jb21tZW50cy5nZW90cmlidS5mci9qcy9lbWJlZC5taW4uanM=>
- sur l'API : <https://www.whatsmyip.org/http-compression-test/?url=aHR0cHM6Ly9jb21tZW50cy5nZW90cmlidS5mci9sYXRlc3Q/bGltaXQ9MTA=>
- sur les flux RSS : <https://www.whatsmyip.org/http-compression-test/?url=aHR0cHM6Ly9jb21tZW50cy5nZW90cmlidS5mci9mZWVkP3VyaT0vYXJ0aWNsZXMvMjAyMS8yMDIxLTA0LTA3X2NhcnRlX3Jlc2VhdV9idXMv>

### Ressources

- voir la [doc d'El Geo Paso](https://elgeopaso.readthedocs.io/fr/latest/deployment/apache.html)
- erreur [Name duplicates previous WSGI daemon definition.](https://github.com/certbot/certbot/issues/4880)

----

## Stockage et sauvegarde

La base de données des commentaires est dans le CDN, ainsi que l'export des commentaires de Disqus : <https://cdn.geotribu.fr/tinyfilemanager.php?p=commentaires>.

De cette façon, elle est accessible par l'équipe (les commentaires sont publics de toute façon) et surtout intégrée au [processus de sauvegarde du CDN](https://github.com/geotribu/minimalist-cdn#script-de-sauvegarde).
