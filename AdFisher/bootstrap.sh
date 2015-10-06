#!/bin/bash


### Install os dependencies
apt-get update

# Required for browsing
apt-get install -y firefox 

# Required for headless testing
apt-get install -y xvfb 

# Required for data analysis
apt-get install -y python-numpy python-scipy python-matplotlib

# Requiured for python dependencies
apt-get install -y python-pip

### Install python dependencies
pip install -r /vagrant/requirements.txt

# Fetch nltk stopwords corpus
python -m nltk.downloader -d /usr/share/nltk_data stopwords
