AdFisher
=========

AdFisher is a tool for running Automated Experiments on Personalized Ad Settings. 

Requirements
-----------
AdFisher runs only on UNIX environments. It uses some standard packages listed here. 
The commands provided for installation work on Ubuntu and OS X. You may find it useful to install packages using `pip`. 
You can install `pip` by following the instructions provided [here](http://pip.readthedocs.org/en/latest/installing.html).
In order to run experiments for data collection, you will need the following packages:

  - selenium```sudo pip install selenium```
  - xvfb ```sudo apt-get install xvfb```
  - xvfbwrapper ```sudo pip install xvfbwrapper```
  - psutil ```sudo pip install psutil```

Selenium is a web-browser automation framework. 
Xvfb allows for headless testing. 
xvfbwrapper is a python wrapper for the same. 
The Xvfb package is not present on OS X, but AdFisher still requires xvfbwrapper.
psutil is required to kill experiments which take too long to complete. Killing them
ensures unnecessary resources are not wasted.
To carry out the data analysis, you require the following packages:
  - numpy, scipy, matplotlib ```sudo pip install numpy scipy matplotlib```*
  - scikit learn ```sudo pip install scikit-learn```
  - stemming ```sudo pip install stemming```
  - nltk ```sudo pip install -U pyyaml nltk```
     - You also need to download the nltk stopwords corpus by typing the following commands in your python interpreter. 
```python
import nltk
nltk.download()
``` 
*pip sometimes cannot install numpy, scipy, matplotlib on Ubuntu. In that case, run 
```sudo apt-get install python-numpy python-scipy python-matplotlib```.
NumPy and SciPy are Python packages for scientific computing. matplotlib enables plotting functions. 
scikit learn has a vast collection of python implemenations of Machine Learning algorithms, 
built on the NumPy, SciPy, and matplotlib packages. 
We use the stemming package to stem words, and the nltk stopwords corpus for identifying stopwords.

**If the scripts stop working after a period of time (~few months), try updating Selenium to the latest version using**
```
sudo pip install -U selenium
```
This generally happens when the browsers get automatically updated and older versions of Selenium can no longer automate them.

Architecture
-----------

AdFisher has two parts - an **examples** folder and a **core** folder. **examples** contains some example scripts to run experiments in addition to some test logs generated from our past experiments. The **core** comprises of several modules which setup the experiments and perform the analyses on the collected data. 

Quick Start
-----------
This repository can be used with [Vagrant](https://www.vagrantup.com/) to quickly get a virtual machine with all the necessary dependencies described above installed.  This can be useful for development and testing experiments.

1. git clone https://github.com/tadatitam/info-flow-experiments
2. vagrant up

This defaults to an Ubuntu Server 14.04 LTS (Trusty Tahr) build and will have the AdFisher source directory synced to /vagrant on the virtual machine. You can SSH into this machine with `vagrant ssh`.
