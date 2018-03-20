#!/bin/bash

echo -e "deb http://security.debian.org/ jessie/updates main contrib\ndeb-src http://security.debian.org/ jessie/updates main contrib\n\ndeb http://ftp.us.debian.org/debian/ jessie main contrib non-free\ndeb-src http://ftp.us.debian.org/debian/ jessie main contrib non-free\n\ndeb http://ftp.us.debian.org/debian/ jessie-backports main contrib non-free\ndeb-src http://ftp.us.debian.org/debian/ jessie-backports main contrib non-free\n" > /etc/apt/sources.list

sudo apt-get update

pkg="python-pip libpython2.7-dev python-daemon python-contextlib2 libmemcached-dev zlib1g-dev"

for i in $pkg; do sudo apt-get -y install $i; done

pip_pkg="tornado pylibmc cython" 

for i in $pip_pkg; do sudo pip install $i; done

sudo pip install cassandra-driver==2.7.2
sudo pip install lockfile==0.12.2

exit 0
