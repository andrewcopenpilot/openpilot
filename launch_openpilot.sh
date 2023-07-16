#!/usr/bin/bash

export MAPBOX_TOKEN=`cat /data/mapboxapikey`
export ZMQ=1

export PASSIVE="0"
exec ./launch_chffrplus.sh

