#!/bin/bash
HOME_DIR="/home/ubuntu/ubuntu-16.04"
SRC_DIR="${HOME_DIR}/src-iso"
NEW_DIR="${HOME_DIR}/new-iso"
ISO_NAME="eCommittee-16.04.2-server-amd64.iso"

echo "PS - Change to \"${NEW_DIR}\""
cd "${NEW_DIR}"

echo "Removing old ISO and md5sum file"
rm -rf ${NEW_DIR}/*

echo "Changing to \"${SRC_DIR}\""
cd "${SRC_DIR}"
echo "PS - Generating md5sum.txt"
#md5sum `find ! -name "md5sum.txt" ! -path "./isolinux/*" -follow -type f` > md5sum.txt
find . -type f -print0 | xargs -0 md5sum > md5sum.txt

cd ..

echo "PS - Greating new ISO file "
mkisofs -D -r -V "eCommittee-16.04.2 Server CD" \
        -cache-inodes \
        -J -l -b isolinux/isolinux.bin \
        -c isolinux/boot.cat \
        -no-emul-boot \
        -boot-load-size 4 -boot-info-table \
        -o ${NEW_DIR}/${ISO_NAME} ${SRC_DIR}

echo "PS - Finished"
