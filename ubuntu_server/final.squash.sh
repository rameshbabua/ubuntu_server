#!/bin/bash
HOME_DIR="/home/ubuntu/ubuntu-16.04"
KEY="${HOME_DIR}/ubuntu-keyring/ubuntu-keyring-2012.05.19/keyrings"
SQUASH="${HOME_DIR}/SquashFS"
FS=${HOME_DIR}/src-iso/install/filesystem.squashfs
FSIZE=${HOME_DIR}/src-iso/install/filesystem.size

echo "PS - Change to $SQUASH"
cd $SQUASH

unsquashfs $FS

cd squashfs-root

echo "Copying key certificates"

cp $KEY/ubuntu-archive-keyring.gpg usr/share/keyrings/ubuntu-archive-keyring.gpg

cp $KEY/ubuntu-archive-keyring.gpg etc/apt/trusted.gpg

cp $KEY/ubuntu-archive-keyring.gpg var/lib/apt/keyrings/ubuntu-archive-keyring.gpg

cat <<EOF >> /etc/apt/sources.list
deb http://archive.ubuntu.com/ubuntu xenial main
deb http://archive.ubuntu.com/ubuntu xenial-updates main
deb http://security.ubuntu.com/ubuntu xenial-security main
EOF

echo "Removing old SquashFS and filesystem.size"
rm $FS $FSIZE

echo "Creating new SquashFS and Filsesystem.size files"
du -sx --block-size=1 ./ | cut -f1 > $FSIZE

mksquashfs ./ $FS

echo "Process Completed"
