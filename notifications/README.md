# Notifications automatisées

## Slack

A la fin du [script de sauvegarde](../backup/README.md), un message d'information est envoyé sur le Slack de Geotribu via un web hook rattaché à l'application Slack Geotribot, liée au compte d'administration de l'espace de travail.

![Notification Slack sauvegarde Geotribu](../docs/_static/img/slack_geotribot_backup_notification.png "Aperçu du message envoyé sur Slack")

### Installation

1. Installer [cURL](https://curl.se/) :

    ```bash
    sudo apt install curl
    ```

2. Copier le fichier `tpl_slack_webhook_backup.json` dans un sous-dossier `notifications` à côté du fichier `backup.sh`
3. Copier le fichier `template.env`, le renommer `.env` à côté du fichier `backup.sh` et renseigner l'URL du web hook (`WEBHOOK_URL_BACKUP`)

### Liens utiles

- interface de gestion de l'application Geotribot : <https://api.slack.com/apps/A020C9Q93BK>
- interface de conception du message : <https://app.slack.com/block-kit-builder/TUKTSG55K>
