Core
=========

The core has several modules that AdFisher uses to perform all aspects of experimentation - unit creation, randomized treatment assignment, and data collection - as well as analysis of the collected data. 

The `adfisher.py` file calls functions from different modules in this folder to perform the experiments and carry out the analysis. The *do_experiment()* function first lays out the overall structure of the experiment - first apply treatments to the units, then collect measurements - and calls upon the **driver** to actually run the experiments. The **driver** uses functions specified in the **web** module to interact with webpages while performing actions specified in the treatment and collecting measurements. All measurements are recorded in a log. Users can add more functions or modules to increase the collection functionalities. For example, like the *GoogleAdsUnit* class defined in `google_ads.py`, you can create any other class and use it as your experimental unit.

For the analysis, the **converter** module reads the log and creates appropriate feature vectors. The feature vectors are then used in the **analysis**. This final module has functions for performing permutation tests, applying machine learning, and plotting various kinds of graphs. The `statistics.py` file defines some of the statistics that we used for our analysis. Users can extend the **analysis** module by adding more ML algorithms, or using different statistics for use with the permutation test.
