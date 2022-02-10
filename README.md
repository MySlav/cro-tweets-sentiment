# cro-tweets-sentiment


Final project of course "Affective computing".


## Description

Source for Annotated tweets in Croatian
https://www.clarin.si/repository/xmlui/handle/11356/1054

We have obtained some tweet IDs and the respective annotations from aforementioned link.

After scraping tweets using tweepy, we have done some cleaning and preprocessing.

We have used a pretrained roBERTa model from Facebook to train a sentiment classifier.

## Getting Started

### Dependencies

tweet_scraper.py

* pandas==1.3.4
* tweepy==4.5.0

AC_RoBERTa.ipynb

* classla==1.1.0
* fastai==1.0.61
* matplotlib==3.2.2 
* numpy==1.19.5 
* pandas==1.3.5          
* scikit_learn==1.0.2
* text_hr==0.20 
* torch==1.10.0+cu111 
* transformers==4.16.2
* tweet_preprocessor==0.6.0
* wordcloud==1.5.0  



## Authors


Mislav Spajić 

[@MySlav](https://github.com/MySlav)

Hrvoje Kopić

[@hrvojekopic](https://github.com/hrvojekopic)