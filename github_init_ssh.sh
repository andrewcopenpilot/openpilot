#!/bin/bash

mkdir /home/comma/.ssh

cat <<EOF > ~/.ssh/config
Host github.com
  User git
  Hostname github.com
  PreferredAuthentications publickey
  IdentityFile /data/id_rsa
EOF
