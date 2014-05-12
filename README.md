WDUD Assistant
=========

WDUD Assistant is a Web Data Usage Detection Tool. 

Requirements
-----------
WDUD Assistant runs only on UNIX environments. It uses some standard packages listed here. 
The commands provided for installation work on Ubuntu.
In order to run WDUD experiments and data collection, you will need the following packages:

  - selenium```pip install selenium```
  - xvfb ```apt-get install xvfb```
  - xvfbwrapper ```pip install xvfbwrapper```

Selenium is a web-browser automation framework. Xvfb allows for headless testing. 
xvfbwrapper is a python wrapper for the same. 
To carry out the data analysis requires the following packages:
  - numpy, scipy, matplotlib ```sudo apt-get install python-numpy python-scipy python-matplotlib```
  - scikit learn ```pip install -U scikit-learn```
  - stemming ```pip install stemming```
  - nltk ```pip install -U pyyaml nltk```
     - You also need to download the nltk stopwords corpus by typing the following commands in your python interpreter. 
```python
import nltk
nltk.download()
``` 

NumPy and SciPy are Python packages for scientific computing. matplotlib enables plotting functions. 
scikit learn has a vast collection of python implemenations of Machine Learning algorithms, 
built on the NumPy, SciPy, and matplotlib packages. 
We use the stemming package to stem words, and the nltk stopwords corpus for identifying stopwords.

Example
-----------

In order to run an experiment, you first need to import the wdud module.
```python
import wdud
```
### Setting up treatments

You can initialize a treatment with its name as follows.
```python
treatment = wdud.Treatment("name")
```
The default treatment is equivalent to the null treatment. Browser instances initiated with this treatment enable behavioral advertisements in the treatment phase.

You can set the gender on Google Ad Settings as part of the treatment.
```python
treatment.set_gender("male")
```
Or add interests on Google Ad Settings. When adding an interest, Google displays  options for which the keyword is a substring. The following line has the browser instance add the first suggested interest when queried for *jobs*.
```python
treatment.add_interest("jobs")
```
You can also specify websites to visit. The *site_file* contains a list of websites in every new line. 
```python
treatment.visit_sites(site_file)
```
##### Populate site_file
The WDUD assistant also allows you to collect the list of sites from any [alexa category](http://www.alexa.com/topsites/category/Top) into a file. For example, the following collects the top 5 websites on Alexa for employment and saves them in *employment.txt*
```python
wdud.collect_sites_from_alexa(output_file="employment.txt", nsites=5, browser="firefox",
        alexa_link="http://www.alexa.com/topsites/category/Top/Business/Employment")
```
### Run Experiment
Once the treatments are set up, you are ready to run the experiment. You must at least specify the list of treatments in order to run the experiment; all other parameters have default values. The *log_file* maintains a log of the experiments. All data from the experiments are stored in this file in a special-character separated format, with each new line containing an entry. The *log_file* is later used to perform data analysis. 

You can specify the number of blocks of the experiment in *blocks*. *samples* specifies the number of browser instances running in a block. *runs* specifies the number of iterations of treatment and collection a single browser instance goes through. 

By setting the *collection_site*, you can change which site to collect Google ads from. As of now, *collection_site* may be either of "toi" (Times of India), "bbc", "guardian", "reuters" or "bloomberg". With *reloads*, you can specify the number of times the collection site is reloaded to collect ads, and *delay* is the time delay in seconds between successive reloads. 

The experiment can be run on either "firefox" or "chrome" browsers as of now, and that can be specified with the *browser* parameter. You can set the timeout of a particular block by specifying the *timeout* parameter. By default, a block times out after 2000 seconds (~30 mins). 
```python
wdud.run_experiment(treatments, log_file="log.txt", blocks=20, samples=2, 
        runs=1, collection_site="toi", reloads=10, delay=5, browser="firefox", timeout=2000)	
```
### Perform Analysis
After collection, the analysis can be carried out as follows. *log_file* specifies the log file from the experiment. *splitfrac* indicates the splitting fraction for the training and testing data. If it is set to 0.1, the first 90% of the blocks are used for training, and the last 10% are used for testing. The number of folds in k-fold cross validation is specified in *nfolds*. *blocks* must be at least as large as *nfolds*. 

*feat_choice* can be either "ads" or "words". It specifies what to the classifier uses as features. The number of features output from the feature selection algorithm is given by *nfeat*. 
```python
wdud.run_analysis(log_file="log.txt", splitfrac=0.1, nfolds=10, 
		feat_choice="ads", nfeat=5, verbose=False)
```
### Full Example
```python
import wdud

site_file = 'employment.txt'

# Collect sites from alexa

wdud.collect_sites_from_alexa(nsites=5, output_file=site_file, browser="firefox", 
	alexa_link="http://www.alexa.com/topsites/category/Top/Business/Employment")

# Set up treatments

treatment1 = wdud.Treatment("female")
treatment1.set_gender("female")
treatment1.visit_sites(site_file)

treatment2 = wdud.Treatment("male")
treatment2.set_gender("male")
treatment2.visit_sites(site_file)

# Run Experiment

wdud.run_experiment(treatments=[treatment2, treatment1], samples=2, blocks=10, reloads=2)

# Analyze Data

wdud.run_analysis()
```