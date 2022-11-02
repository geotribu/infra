#!/bin/bash

# Create a release with compressed CDN images, then send a notification to Slack

# Le petit manuel
if [ "$1" = "-h" ] ; then
    echo "Créer un fichier .env avec les paramètres de configuration puis ./$(basename $0)"
    echo "Show this help: ./$(basename "$0") -h"
    exit 0
fi

# on lit le fichier de configuration
SCRIPT_FOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
. "$SCRIPT_FOLDER/.env"

# -- Variables -------------
_today=$(date +"%Y-%m-%d")
_tomonth=$(date +"%Y.%m")

# -- Script ----------------

# Generate archive of compressed static files
: ' Mémo des options :
    –c : crée un archive.
    –z : compresse avec gzip.
    –v : mode verbeux, affiche la progression.
    –f : permet de spécifier le nom du fichier
'
tar -zcf "$HOME/backups/cdn/bkp_cdn_${_today}.tar.gz" -C /var/www/geotribu/cdn/ images/
FILE_SIZE=$(du --human-readable "$HOME/backups/cdn/bkp_cdn_${_today}.tar.gz" | cut -f1)

# Move to the website repository
cd /var/www/geotribu/website/sources/ || exit
# Update git
git pull --ff-only --tags
# disable GitHub CLI prompts
gh config set prompt disabled
# Create release
gh release create "$_tomonth" "$HOME"/backups/cdn/bkp_cdn_"${_today}".tar.gz --title "Sauvegarde $_tomonth" --generate-notes


# -- Slack Notification

# prepare message
sed "s/{{ ARCHIVE_SIZE }}/$FILE_SIZE/; s/{{ TAG }}/$_tomonth/" "$HOME"/scripts/geotribu-backup/notifications/tpl_slack_webhook_backup.json > "$HOME"/scripts/geotribu-backup/notifications/slack_webhook_backup_message_"$_today".json

# send message to Slack web hook
curl -X POST \
     -H 'Content-type: application/json' \
     --data "@$HOME/scripts/geotribu-backup/notifications/slack_webhook_backup_message_$_today.json" \
     "$WEBHOOK_URL_BACKUP"
