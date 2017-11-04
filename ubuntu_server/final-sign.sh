BUILD=/home/ubuntu/ubuntu-16.04/src-iso
APTDIR=/home/ubuntu/ubuntu-16.04/original/apt-ftparchive
APTCONF=$APTDIR/release.conf
DISTNAME=xenial

apt-ftparchive -c $APTCONF generate $APTDIR/apt-ftparchive-deb.conf
apt-ftparchive -c $APTCONF generate $APTDIR/apt-ftparchive-udeb.conf
apt-ftparchive -c $APTCONF generate $APTDIR/apt-ftparchive-extras.conf
apt-ftparchive -c $APTCONF release $BUILD/dists/$DISTNAME > $BUILD/dists/$DISTNAME/Release

gpg --default-key "877B7FC0" --output $BUILD/dists/$DISTNAME/Release.gpg -ba $BUILD/dists/$DISTNAME/Release

cd $BUILD/dists/$DISTNAME/
find . -type f -print0 | xargs -0 md5sum > md5sum.txt
