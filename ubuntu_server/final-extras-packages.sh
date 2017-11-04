#!/bin/bash
HOME_DIR="/home/ubuntu/ubuntu-16.04"
SRC_DIR="${HOME_DIR}/src-iso"
NEW_DIR="${HOME_DIR}/new-iso"
DEB_DIR="${HOME_DIR}/debs"
EXTRAS_DIST="${SRC_DIR}/dists/stable/extras/binary-amd64"
EXTRAS_POOL="${SRC_DIR}/pool/extras"
ORI_DIR="${HOME_DIR}/original"

echo "PS - Change to \"${HOME_DIR}\""
cd "${HOME_DIR}"

echo "PS - Checking directories"
if [ ! -e "${DEB_DIR}" ]; then
    echo "Error: Please make sure your debs are located at "
    echo " \"${DEB_DIR}\""
    exit 1
fi

echo "Removing old debfiles and Packages"
rm -rf ${EXTRAS_DIST}/*
rm -rf ${EXTRAS_POOL}/*

echo "Creating directories for extra:"
cd ${SRC_DIR}
mkdir -p dists/stable/extras
mkdir -p dists/stable/extras/binary-amd64

echo "PS - Copying all debs to \"${EXTRAS_POOL}\""
rsync -avz ${DEB_DIR}/* ${EXTRAS_POOL}/

echo "Moving configuration files"
rsync -avz "${ORI_DIR}"/isolinux/* "${SRC_DIR}"/isolinux/ 
rsync -avz "${ORI_DIR}"/preseed/* "${SRC_DIR}"/preseed/

echo "PS - Generating Packages.gz for extras"
cd ${SRC_DIR}
for component in extras main; 
do
	sudo apt-ftparchive packages "${SRC_DIR}/pool/$component/" > "${SRC_DIR}/dists/stable/$component/binary-amd64/Packages"
	gzip -c "${SRC_DIR}/dists/stable/$component/binary-amd64/Packages" | sudo tee "${SRC_DIR}/dists/stable/$component/binary-amd64/Packages.gz" > /dev/null
done

echo "PS - Finished"
