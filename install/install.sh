#!/bin/bash

set -e

function log() {
    echo $@
}

if (( $EUID != 0 )); then
   echo "This script must be run as root" 
   exit 1
fi

BASE_DIR=/opt/mc
FILE_DIR=$(realpath $(dirname $0))
SERVER_DIR=$BASE_DIR/server

log "Installing dependancies"
apt install -y openjdk-11-jre-headless screen wget

log "Setting up folders"
mkdir -p $SERVER_DIR $SERVER_DIR/plugins
cd $SERVER_DIR
echo "eula=True" > eula.txt

log "Downloading server"
wget https://cdn.getbukkit.org/craftbukkit/craftbukkit-1.16.3.jar 

if [ -f "$FILE_DIR/assets/plugins.txt" ]; then
    log "Downloading plugins"
    for plugin in $(grep . $FILE_DIR/assets/plugins.txt); do
        wget -P plugins $plugin;
    done
else
    log "No plugins.txt, skipping downloading plugins"
fi

log "Creating minecraft user"
adduser --system --home $BASE_DIR --group minecraft
chown -R minecraft.minecraft $BASE_DIR

if [ -f "$FILE_DIR/assets/minecraft.service" ]; then
    log "Creating systemd service minecraft@server"
    cp $FILE_DIR/assets/minecraft.service /etc/systemd/system/minecraft@.service
else
    log "No minecraft.service found, skipping systemd service creation"
fi

log "Copying configuration files"
cp -r $FILE_DIR/config/. $BASE_DIR/server

cd $OLDPWD
log "Done."