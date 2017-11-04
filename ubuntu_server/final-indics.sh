cd /home/ubuntu/ubuntu-16.04/original/indices/
DIST=xenial
for SUFFIX in extra.main main main.debian-installer restricted restricted.debian-installer; do
  wget http://archive.ubuntu.com/ubuntu/indices/override.$DIST.$SUFFIX
done
