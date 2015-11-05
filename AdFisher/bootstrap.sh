#!/bin/bash


### Install os dependencies
apt-get update

# Install gui
apt-get install -y ubuntu-desktop gnome-session-flashback

# Required for browsing
apt-get install -y firefox 

# Required for headless testing
apt-get install -y xvfb 

# Required for data analysis
apt-get install -y python-numpy python-scipy python-matplotlib

# Requiured for python dependencies
apt-get install -y python-pip python-dev

# Required for pyre2 dependencies
apt-get install -y git build-essential
cd ~
git clone https://code.googlesource.com/re2
cd re2
make test
sudo make install


### Install python dependencies
sudo pip install -r /vagrant/requirements.txt

# Fetch nltk stopwords corpus
python -m nltk.downloader -d /usr/share/nltk_data stopwords
