# Analyzing and predicting emotions generated by internet newspaper articles
I decided to learn more about how deep learning NLP works
###### Used tools:
- tensorflow 1.14.0 (training)
- Google cloud platform (hosting notebooks and api)
- python3 (data processing)
- flask (api)
- javascript (chrome extension)

# Quickstart
- python -m pip install -r requirements.txt
- scraping data: you need to download [chrome driver](https://sites.google.com/a/chromium.org/chromedriver/downloads)

#### Quickstart - downloading more data
Open /data/old_articles.ipynb, in the first cell page change numbers you want to scrap. Notebook firstly goes through all index sites (each index site has 25 articles) takes urls of all those articles, and then for each url scraps the content. So if you specified from 1 to 2 it will go to two index sites, collects urls (50 overall), and for each url it will try to scrap the content of the article.

#### Quickstart - training model
If you have scrapped more data you have to run all notebooks from 1-4, and then go to the 5th one and play around with tensorflow.

#### Quickstart - api and extension
- for api run python api/endpoint.py
- for chrome extension you need to turn on the developer mode, then visit chrome://extensions and load unpacked directory /extension.
- Then you just need to change request url in content.js, 79 line for 127.0.0.1:5000.

## Introduction
I was looking for an idea for a NLP project, that could be both challenging, so I could learn as much as I can about
natural language processing, and as close as it could be to real life task. I came with an idea, with witch the internet news publishers would be interested in - what would be a response generated by the article they publish on a website. The reason why
it could be useful is that in this example (like in many others) very often just a certain part of an article is available
for everyone - if you want to read the whole you have to buy some kind of premium subscription, which is very important
from the business perspective.
Because I do not have data about page views or users who bought subscription I decided to use information which is hidden inside the comments. I assume that the better (stronger) response is, the more subscriptions will be sold. But I think that just two measurements - of comments and likes - won't be sufficient, so I want to add one more metric - human emotions.
As we all know the more emotionally engaged we are in something (take a hobby as an example) the more money we are eager to spend on it. Hence, the more emotions an article evokes in us, the more likely we are to buy a premium (and uncover the rest of the article).
So I take a standpoint of data scientist in this company and want to answer a question asked by the executive:
> "Which articles will give us the most subscriptions, you smart ass?"

## Steps

#### 1. Scrap data
For each old index page (list) of 'the newest articles' go to listed url and scrap the article and comments below it. I also found in source code that some of them are labeled as suspicious, so that can be useful in terms of model accuracy. I also had to handle login and premium account, since content of most of those articles is limited to the first few paragraphs.
> Notebook: data/old_articles.ipynb

> Data: data/comments/*

#### 2. Try to label records
The main idea behind most NLP tasks is that we assume that word meaning and word context is the same thing. Thanks to this assumption we can analyze text better and find a way to define word context in a code in such way that it will represent the word meaning. Those definitions (vectors) we can then use to things like calculating word similarities or for a better representation of a word corpus, and all of these things we will learn in this project.
I want to use this task to learn more about core concepts of NLP, there are much easier ways to label records which I will explain later on.

##### &nbsp;&nbsp;&nbsp;2.1. Singular value decomposition
The fastest and the simple one. By reducing dimension (length) of word
vectors with SVD each row (which represents one word) will shrink so the
values inside have to change. Those vectors should now represent word embedding.
> Notebook: labeling/SVD.ipynb

##### &nbsp;&nbsp;&nbsp;2.2. Word2Vec
This time to obtain those vectors we will create neural network with just one hidden layer, feed it with pairs train_word - surrounding_word (a Skip Gram model). The hidden layer then becomes our word embedding which tells us about the context of this word.
> Notebook: labeling/Word2Vec.ipynb

##### &nbsp;&nbsp;&nbsp;2.3. GloVe
In this case we use global word to word co-occurrence counts, create a matrix with words as rows and co-occurrences as columns, reduce dimensions and normalize counts.
> Notebook: labeling/GloVe.ipynb

Results didn't satisfy me, so I decided to create my own way of labeling, very simple but efficient: I picked words which I associate with emotions and found many others on internet: [link](http://exp.lobi.nencki.gov.pl/nawl-analysis).
> Notebook: 1) process_data.ipynb

#### 3. Train model to predict emotions from the article
This is the main purpose of this project - being able to predict user engagement before publishing the article. Used features:
- title
- image description
- content
- dummy dates
- division category
- author category
- media type

All text features needed to be lemmatized
> Notebook: 2) lemmatize_articles.ipynb

I had also to filter word2vec downloaded from [link](http://dsmodels.nlp.ipipan.waw.pl/)
> Notebook: 3) filter_word2vec.ipynb

And, of course, apply word2vec to four columns
> Notebook: 4) apply_word2vec.ipynb

##### &nbsp;&nbsp;&nbsp; 4.1. Try to predict emotions
The only thing I was able to predict were emotions - the most probable reason is that I used words inside comments to describe emotions, the same words could be found in the articles itself.
> Notebook: 5) train_model.ipynb

##### &nbsp;&nbsp;&nbsp; 4.2. Try to predict other measurements - replies and reactions
It didn't work for me, I was not able to predict neither reactions nor replies. You can try by on own in notebook cited above, you just have to change selected_label variable value.

#### 4. Write simple flask API with two endpoints for each model
The api can be found in
> /api

I split it into four important files, endpoint (data is received and returned), cleaner (basic cleaning), features (calculate features), models (calculate predictions)

#### 5. Write chrome extension
The last thing needed for the project to be considered completed - easy user interface. While writing that it works locally, I added it to chrome store and it has to be validated. It is inside
> /extension

directory, data scrapping and sending a request is inside content.js file.

#### 6. Further steps

###### 1) Find people who got paid to write rage comments

As I wrote at the beginning I found that some comments are flagged as "suspicious". We all know that there are companies who get paid for writing comments for specific purposes, maybe I could cluster all users into a real ones and those hired by companies (or bots?). Useful features:
- sentiment
- regularity
- connections with other commentators
- vocabulary
- response speed
- posting hours

###### 2) Try again training model for number of replies label with different settings
Try:
- Batch normalization
- Adam optimizer
- zero centered - data
- lower learning rate
