WDUD Assistant
=========

WDUD Assistant is a Web Data Usage Detection Tool. 

Requirements
-----------
WDUD Assistant runs only on UNIX environments. It uses some standard packages listed here. The commands provided for installation are for Ubuntu.
In order to run WDUD experiments and data collection, you will need the following packages:

  - selenium```pip install selenium```
  - xvfb ```apt-get install xvfb```
  - xvfbwrapper ```pip install xvfbwrapper```

Selenium is a web-browser automation framework. Xvfb allows for headless testing. xvfbwrapper is a python wrapper for the same. To carry out the data analysis requires the following packages:
  - numpy, scipy, matplotlib ```sudo apt-get install python-numpy python-scipy python-matplotlib```
  - scikit learn ```pip install -U scikit-learn```
  - stemming ```pip install stemming```
  - nltk ```pip install -U pyyaml nltk```
     - You also need to download the nltk stopwords corpus by typing the following commands in your python interpreter. 
```python
import nltk
nltk.download()
``` 

NumPy and SciPy are Python packages for scientific computing. matplotlib enables plotting functions. scikit learn has a vast collection of python implemenations of Machine Learning algorithms, built on the NumPy, SciPy, and matplotlib packages. We use the stemming package to stem words, and the nltk stopwords corpus for identifying stopwords.

Example: Running an Experiment
-----------

```python
import wdud

site_file = 'list_of_sites.txt'
log_file = 'log.example.txt'

## Collect sites from alexa
wdud.collect_sites_from_alexa(nsites=5, output_file=site_file, 
	alexa_link="http://www.alexa.com/topsites/category/Top/Health/Addictions/Substance_Abuse")
	
## Set up treatments
treatment1 = wdud.Treatment('null')
treatment2 = wdud.Treatment('example')
treatment2.add_interest("wine")
treatment2.add_gender("male")
treatment2.add_site_file(site_file)

## Run Experiment
wdud.begin_experiment(treatments=[treatment1, treatment2], 
        samples=2, blocks=1, reloads=2, log_file=log_file)
```

Example: Running Data Analysis
----------
```python
import analysis.functions as analyst

## Analyze Data
coll = analyst.get_ads_from_log(log_file)
print "Number of blocks collected:", len(coll[0])
analyst.MLAnalysis(coll, featChoice='ads')
```