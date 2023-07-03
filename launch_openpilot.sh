#!/usr/bin/bash

export MAPBOX_TOKEN=`cat /data/mapboxapikey`

export PASSIVE="0"
exec ./launch_chffrplus.sh

