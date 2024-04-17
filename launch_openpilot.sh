#!/usr/bin/bash

export MAPBOX_TOKEN=`cat /data/mapboxapikey`
export ZMQ=1

exec ./launch_chffrplus.sh
