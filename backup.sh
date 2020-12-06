#!/bin/bash

# Create a release with compressed CDN images

# -- Variables -------------
_today=`date +"%Y-%m-%d"`
_tomonth=`date +"%Y.%m"`

# -- Script ----------------

# Generate archive of compressed static files
tar -zcvf "$HOME/backups/cdn/bkp_cdn_${_today}.tar.gz" -C /var/www/geotribu/cdn/ images/

# Move to the website repository
cd /var/www/geotribu/website/
# Update git
git pull --ff-only --tags
# disable GitHub CLI prompts
gh config set prompt disabled
# Create release
gh release create $_tomonth $HOME/backups/cdn/bkp_cdn_${_today}.tar.gz --title "Sauvegarde $_tomonth"
