#!/bin/bash
HOME_DIR="/home/ubuntu/ubuntu-16.04"
STAGE=/mnt/iso
ORI_DIR="${HOME_DIR}/original"
SRC_DIR="${HOME_DIR}/src-iso/"

echo "PS - Change to \"${HOME_DIR}\""
cd "${HOME_DIR}"

echo "PS - Checking directories"
mkdir -p "${SRC_DIR}"

echo "PS - Mounting ISO file"
sudo umount $STAGE
sudo mount -o loop,ro "${ORI_DIR}"/ubuntu-16.04.2-server-amd64.iso $STAGE

echo "PS - Copying all files from ISO to new directory"
rsync -avzb $STAGE/ "${SRC_DIR}"
rsync -avzb "${ORI_DIR}"/postinstall "${SRC_DIR}"

echo "PS - Unmounting ISO file"
sudo umount $STAGE

echo "PS - Finished"
