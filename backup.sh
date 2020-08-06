#!/bin/bash

# Create a release with compressed CDN images

# Store current date
_today=`date +"%Y-%m-%d"`

# Generate archive
tar -zcvf "~/backups/cdn/bkp_cdn_${_today}.tar.gz" -C /var/www/geotribu/cdn/ images/
