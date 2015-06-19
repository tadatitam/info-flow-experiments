AdFisher
=========

AdFisher is a tool for running Automated Experiments on Personalized Ad Settings. 

Requirements
-----------
AdFisher runs only on UNIX environments. It uses some standard packages listed here. 
The commands provided for installation work on Ubuntu and OS X. You may find it useful to install packages using `pip`. 
You can install `pip` by following the instructions provided [here](http://pip.readthedocs.org/en/latest/installing.html).
In order to run experiments for data collection, you will need the following packages:

  - selenium ```sudo pip install selenium```
  - xvfb ```sudo apt-get install xvfb``` (Not needed for MacOS) 
  - xvfbwrapper ```sudo pip install xvfbwrapper```
  - psutil ```sudo pip install psutil```

Selenium is a web-browser automation framework. Xvfb allows for headless testing. 
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
(When the window opens up, click "Corpra" and scroll down to "stopwards". Click on "stopwards" to make sure it is highlighted. Once "stopwards" is highlighted, click "Download".)
*pip sometimes cannot install numpy, scipy, matplotlib on Ubuntu. In that case, run 
```sudo apt-get install python-numpy python-scipy python-matplotlib```.
NumPy and SciPy are Python packages for scientific computing. matplotlib enables plotting functions. 
scikit learn has a vast collection of python implemenations of Machine Learning algorithms, 
built on the NumPy, SciPy, and matplotlib packages. 
We use the stemming package to stem words, and the nltk stopwords corpus for identifying stopwords.


Architecture
-----------

AdFisher has two parts - an **examples** folder and a **core** folder. **examples** contains some example scripts to run experiments in addition to some test logs generated from our past experiments. The **core** comprises of several modules which setup the experiments and perform the analyses on the collected data. 
